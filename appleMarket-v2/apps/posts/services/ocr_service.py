import os

# [중요] PaddlePaddle C++ 백엔드 및 oneDNN 버그 방지 옵션 (최상단)
os.environ['FLAGS_enable_pir_api'] = '0'
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_use_onnx'] = '0'

import cv2
import numpy as np
from PIL import Image
import paddle
from paddleocr import PaddleOCR

# C++ 레벨에서 oneDNN/PIR이 켜지는 것 방지
try:
    paddle.base.core.set_prim_eager_enabled(False)
except Exception:
    pass

# 모델 로딩이 느리므로 싱글톤으로 한 번만 초기화
_ocr_instance = None


def get_ocr():
    """PaddleOCR 인스턴스를 lazy-load 방식으로 반환"""
    global _ocr_instance
    if _ocr_instance is None:
        # enable_mkldnn=False를 반드시 명시해야 oneDNN C++ 에러가 발생하지 않습니다.
        _ocr_instance = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=True,
            lang='korean',
            enable_mkldnn=False,  # <--- [핵심 해결책] oneDNN 가속 비활성화
            use_gpu=False,        # CPU 연산 시 C++ 엔진 안정화
        )
    return _ocr_instance


def preprocess_image(image_path):
    """OCR 인식률을 높이기 위한 이미지 전처리
    
    - 그레이스케일 변환
    - 저해상도 이미지 확대
    - CLAHE로 대비 향상
    - 노이즈 제거
    - Adaptive Threshold로 이진화
    """
    # 이미지 읽기 (한글 경로 대응)
    img_array = np.fromfile(image_path, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        pil_img = Image.open(image_path).convert('RGB')
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # 1. 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 저해상도 이미지 확대 (긴 변 기준 1500px)
    h, w = gray.shape
    if max(h, w) < 1000:
        scale = 1500 / max(h, w)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # 3. CLAHE로 대비 향상
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # 4. 노이즈 제거
    denoised = cv2.fastNlMeansDenoising(gray, h=15)

    # 5. 3채널로 다시 변환 (PaddleOCR는 컬러 이미지 기대)
    result = cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)
    return result


def extract_text_from_image(image_path):
    """이미지에서 텍스트를 추출하여 문자열 리스트로 반환"""
    processed = preprocess_image(image_path)
    ocr = get_ocr()

    texts = []
    try:
        # PaddleOCR 3.x / PaddleX 예측
        result = ocr.predict(processed)
        if result:
            for page in result:
                # dict 구조 또는 객체 구조 대응
                if isinstance(page, dict):
                    rec_texts = page.get('rec_texts', [])
                elif hasattr(page, 'get'):
                    rec_texts = page.get('rec_texts', [])
                elif hasattr(page, 'rec_texts'):
                    rec_texts = page.rec_texts
                else:
                    rec_texts = page['rec_texts'] if 'rec_texts' in page else []
                
                texts.extend(rec_texts)
    except Exception:
        # PaddleOCR 2.x 방식 fallback
        result = ocr.ocr(processed, cls=True)
        if result and result[0]:
            for line in result[0]:
                if isinstance(line, (list, tuple)) and len(line) > 1:
                    texts.append(line[1][0])

    return texts
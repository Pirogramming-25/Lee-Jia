"""OCR 결과에서 영양 성분을 파싱하는 후처리 로직"""
import re


def parse_nutrition(texts):
    """OCR로 추출한 텍스트 리스트에서 칼로리, 탄단지 정보를 추출.

    Returns:
        dict: {
            'calories': int | None,  # kcal
            'carbs': float | None,   # g로 통일
            'protein': float | None, # g로 통일
            'fat': float | None,     # g로 통일
        }
    """
    # 텍스트 하나로 합치고 공백/특수문자 정리
    full_text = ' '.join(texts)
    # OCR이 종종 헷갈리는 문자 정리 (콤마 → 온점)
    full_text = full_text.replace(',', '.')

    return {
        'calories': _find_calories(full_text),
        'carbs': _find_nutrient(full_text, ['탄수화물', '탄수']),
        'protein': _find_nutrient(full_text, ['단백질']),
        'fat': _find_fat(full_text),
    }


def _find_calories(text):
    """칼로리(kcal) 값을 정수로 추출"""
    patterns = [
        r'열\s*량[^\d]{0,10}(\d+(?:\.\d+)?)',
        r'칼\s*로\s*리[^\d]{0,10}(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s*(?:kcal|㎉|Kcal|KCAL)',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return int(float(m.group(1)))
    return None


def _find_nutrient(text, keywords):
    """탄수화물/단백질 함량을 g으로 통일하여 반환 (mg → g 변환)"""
    for kw in keywords:
        # "탄수화물 45g" / "탄수화물 45 g" / "탄수화물: 45g" 등
        pattern = rf'{kw}[^\d]{{0,10}}(\d+(?:\.\d+)?)\s*(mg|g)'
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            value = float(m.group(1))
            unit = m.group(2).lower()
            if unit == 'mg':
                value = value / 1000
            return round(value, 2)
    return None


def _find_fat(text):
    """지방 함량 추출 - '포화지방', '트랜스지방'과 구분"""
    # '포화'/'트랜스'가 앞에 붙지 않은 '지방'만 매칭
    pattern = r'(?<!포화)(?<!트랜스)(?<!불포화)지\s*방[^\d]{0,10}(\d+(?:\.\d+)?)\s*(mg|g)'
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        value = float(m.group(1))
        unit = m.group(2).lower()
        if unit == 'mg':
            value = value / 1000
        return round(value, 2)
    return None
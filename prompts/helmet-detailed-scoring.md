# 安全帽佩戴详细评分提示词配置

## 多维度评分提示词

```prompt
请根据以下评分标准，对图片中的人是否佩戴安全帽进行详细评分：

1. 安全帽佩戴情况（40分）：
   - 40分：清晰可见完整的安全帽
   - 30分：部分可见安全帽
   - 20分：疑似安全帽
   - 10分：无安全帽

2. 头发可见度（20分）：
   - 20分：完全看不到头发
   - 15分：少量头发可见
   - 10分：部分头发可见
   - 5分：明显可见头发

3. 面部特征（10分）：
   - 10分：面部特征被安全帽遮挡
   - 5分：部分面部特征可见
   - 0分：面部特征清晰可见

4. 安全帽颜色（10分）：
   - 10分：标准安全帽颜色（黄色、红色、白色等）
   - 5分：非标准颜色
   - 0分：无安全帽

5. 安全帽形状（10分）：
   - 10分：标准安全帽形状
   - 5分：形状异常
   - 0分：无安全帽

6. 佩戴位置（10分）：
   - 10分：正确佩戴位置
   - 5分：位置异常
   - 0分：无安全帽

请根据以上标准进行评分，并返回以下格式的JSON：
{
    "helmet_score": <总分，0-100之间的整数>,
    "detailed_scores": {
        "helmet_visibility": <安全帽佩戴情况得分，0-40>,
        "hair_visibility": <头发可见度得分，0-20>,
        "face_visibility": <面部特征得分，0-10>,
        "helmet_color": <安全帽颜色得分，0-10>,
        "helmet_shape": <安全帽形状得分，0-10>,
        "helmet_position": <佩戴位置得分，0-10>
    }
}
```

## 输出格式配置

```json
{
    "type": "object",
    "properties": {
        "helmet_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
        },
        "detailed_scores": {
            "type": "object",
            "properties": {
                "helmet_visibility": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 40
                },
                "hair_visibility": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 20
                },
                "face_visibility": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 10
                },
                "helmet_color": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 10
                },
                "helmet_shape": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 10
                },
                "helmet_position": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 10
                }
            },
            "required": [
                "helmet_visibility",
                "hair_visibility",
                "face_visibility",
                "helmet_color",
                "helmet_shape",
                "helmet_position"
            ]
        }
    },
    "required": ["helmet_score", "detailed_scores"]
}
``` 
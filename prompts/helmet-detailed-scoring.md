# 安全帽佩戴详细评分提示词配置

## 多维度评分提示词

```prompt
请分析图片中的人是否佩戴安全帽，并按照以下步骤进行评分：

请先仔细观察图片，然后按照以下步骤一步步分析和评分：

步骤1：判断安全帽佩戴情况（40分）
- 首先观察图片中是否有安全帽
- 如果能清晰看到完整的安全帽，给40分
- 如果只能部分看到安全帽，给30分
- 如果只能看到疑似安全帽的物体，给20分
- 如果完全看不到安全帽，给10分
推理示例："我能清楚地看到图中人物头上佩戴了一顶黄色安全帽，帽子轮廓完整清晰，因此安全帽佩戴情况得分为40分。"

步骤2：评估头发可见度（20分）
- 观察安全帽下是否可以看到头发
- 如果完全看不到头发，给20分
- 如果只有少量头发可见，给15分
- 如果部分头发可见，给10分
- 如果大量头发明显可见，给5分
推理示例："安全帽下有少量头发从帽子边缘露出，头发可见度得分为15分。"

步骤3：判断面部特征与安全帽的关系（10分）
- 观察面部上方是否被安全帽遮挡
- 如果面部特征被安全帽正确遮挡，给10分
- 如果部分面部特征可见，给5分
- 如果面部特征清晰可见没有遮挡，给0分
推理示例："此人的额头和眉毛上方区域被安全帽正确遮挡，面部特征得分为10分。"

步骤4：评估安全帽颜色（10分）
- 观察安全帽颜色是否符合标准
- 如果是标准安全帽颜色（黄色、红色、白色等），给10分
- 如果是非标准颜色，给5分
- 如果没有安全帽，给0分
推理示例："安全帽是标准的黄色，符合工地安全帽颜色规范，安全帽颜色得分为10分。"

步骤5：评估安全帽形状（10分）
- 观察安全帽形状是否符合标准
- 如果是标准安全帽形状，给10分
- 如果形状异常，给5分
- 如果没有安全帽，给0分
推理示例："安全帽呈现出标准的圆弧形状，有坚硬外壳，形状正常，安全帽形状得分为10分。"

步骤6：评估佩戴位置（10分）
- 观察安全帽是否正确佩戴在头顶
- 如果佩戴位置正确，给10分
- 如果位置异常（如歪斜、太高或太低），给5分
- 如果没有安全帽，给0分
推理示例："安全帽正确佩戴在头顶位置，没有歪斜，佩戴位置得分为10分。"

步骤7：计算总分
将上述6个方面的分数相加，得到总分（0-100之间）
推理示例："总分 = 40 + 15 + 10 + 10 + 10 + 10 = 95分"

请根据以上步骤进行评分，对每个评分项给出明确的理由，最后返回以下格式的JSON：
{
    "helmet_score": <总分，0-100之间的整数>,
    "detailed_scores": {
        "helmet_visibility": <安全帽佩戴情况得分，0-40>,
        "hair_visibility": <头发可见度得分，0-20>,
        "face_visibility": <面部特征得分，0-10>,
        "helmet_color": <安全帽颜色得分，0-10>,
        "helmet_shape": <安全帽形状得分，0-10>,
        "helmet_position": <佩戴位置得分，0-10>
    },
    "reasoning": <对评分的简要解释，不超过200字>
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
        },
        "reasoning": {
            "type": "string"
        }
    },
    "required": ["helmet_score", "detailed_scores", "reasoning"]
}
``` 
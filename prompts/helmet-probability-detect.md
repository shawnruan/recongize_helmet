# 安全帽佩戴检测与概率评估提示词配置

## 合并的安全帽检测与概率提示词

```prompt
请分析图片中的人是否佩戴安全帽，执行以下步骤：

1. 检测图片中人和安全帽的位置，并给出精确坐标。坐标格式为 [x1, y1, x2, y2]，表示包围人或安全帽的矩形框的左上角和右下角坐标。

2. 对每个检测到的人，判断其是否佩戴安全帽，并给出一个1到100之间的整数，表示佩戴安全帽的概率。
   - 数值越接近100，表示此人佩戴安全帽的可能性越大
   - 数值越接近1，表示此人佩戴安全帽的可能性越小

3. 判断安全帽是否正确佩戴在人的头部。

请返回符合以下格式的JSON：
{
    "detections": [
        {
            "type": "person",  // 可以是 "person" 或 "helmet"
            "bbox": [x1, y1, x2, y2],  // 坐标值
            "helmet_score": <佩戴安全帽的概率分数，1到100之间的整数>,
            "is_correctly_worn": <true/false>  // 安全帽是否正确佩戴
        },
        // 可能有多个检测结果
    ],
    "helmet_score": <整体佩戴安全帽的概率分数，1到100之间的整数>
}

注意：
- 如果图片中没有检测到人或安全帽，请返回空的detections数组
- helmet_score为整体评估分数，即使有多个人也只需要一个总体分数
- 每个检测项的is_correctly_worn表示该人的安全帽是否正确佩戴
```

## 输出格式配置

```json
{
    "type": "object",
    "properties": {
        "detections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["person", "helmet"]
                    },
                    "bbox": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "minItems": 4,
                        "maxItems": 4
                    },
                    "helmet_score": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "is_correctly_worn": {
                        "type": "boolean"
                    }
                },
                "required": ["type", "bbox", "helmet_score", "is_correctly_worn"]
            }
        },
        "helmet_score": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
        }
    },
    "required": ["detections", "helmet_score"]
}
```

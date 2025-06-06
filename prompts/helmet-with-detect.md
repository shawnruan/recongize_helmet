# 安全帽检测坐标提示词配置

## 基础检测提示词

```prompt
分析图片中人物佩戴安全帽的情况。
首先检测人物位置及安全帽位置，然后判断是否佩戴安全帽。
请按以下JSON格式返回：
{
    "person_coordinates": {
        "x1": <人物边界框左上角x坐标>,
        "y1": <人物边界框左上角y坐标>,
        "x2": <人物边界框右下角x坐标>,
        "y2": <人物边界框右下角y坐标>
    },
    "helmet_coordinates": {
        "x1": <安全帽边界框左上角x坐标>,
        "y1": <安全帽边界框左上角y坐标>,
        "x2": <安全帽边界框右下角x坐标>,
        "y2": <安全帽边界框右下角y坐标>
    },
    "helmet": <是否佩戴安全帽，1表示佩戴，0表示未佩戴>
}
注意：坐标值为0到1之间的小数，表示相对于图片尺寸的比例位置。如果未检测到安全帽，则helmet_coordinates中的值均为0。
```

## 输出格式配置

```json
{
    "type": "object",
    "properties": {
        "person_coordinates": {
            "type": "object",
            "properties": {
                "x1": {"type": "integer", "minimum": 0, "maximum": 1},
                "y1": {"type": "integer", "minimum": 0, "maximum": 1},
                "x2": {"type": "integer", "minimum": 0, "maximum": 1},
                "y2": {"type": "integer", "minimum": 0, "maximum": 1}
            },
            "required": ["x1", "y1", "x2", "y2"]
        },
        "helmet_coordinates": {
            "type": "object",
            "properties": {
                "x1": {"type": "integer", "minimum": 0, "maximum": 1},
                "y1": {"type": "integer", "minimum": 0, "maximum": 1},
                "x2": {"type": "integer", "minimum": 0, "maximum": 1},
                "y2": {"type": "integer", "minimum": 0, "maximum": 1}
            },
            "required": ["x1", "y1", "x2", "y2"]
        },
        "helmet": {
            "type": "integer",
            "enum": [0, 1]
        }
    },
    "required": ["helmet"]
}
```

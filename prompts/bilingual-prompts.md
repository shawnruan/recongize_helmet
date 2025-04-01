# 中英双语安全帽检测提示词配置

## 双语检测提示词

```prompt
请分析图片并判断人物是否佩戴安全帽。
Please analyze the image and determine if the person is wearing a safety helmet.

规则 / Rules:
- 必须是标准安全帽 / Must be a standard safety helmet
- 必须正确佩戴 / Must be worn correctly

返回格式 / Return format:
{
    "helmet": <1表示佩戴，0表示未佩戴 / 1 for wearing, 0 for not wearing>
}
```

## 输出格式配置

```json
{
    "type": "object",
    "properties": {
        "helmet": {
            "type": "integer",
            "enum": [0, 1]
        }
    },
    "required": ["helmet"]
}
``` 
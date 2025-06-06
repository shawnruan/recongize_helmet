# 安全帽检测和数量统计提示词

## 数量统计提示词

```prompt
Analyze the people and safety helmets in the image:

1. First identify all people in the image
2. Determine whether each person is wearing a safety helmet
3. Count the following:
   - Number of people without safety helmets
   - Number of people wearing safety helmets
   - Total number of people in the image

Important notes:
- Each person should be counted as either wearing or not wearing a helmet
- Ensure that "people without helmets + people with helmets = total people"
- If any person is not wearing a safety helmet, consider it a safety alert

Return only a JSON in the following format without any explanation:
{
    "head": <number of people without safety helmets>,
    "helmet": <number of people with safety helmets>,
    "person": <total number of people>,
    "alert": <whether there are people without safety helmets, represented as true or false>
}
```

## 输出格式配置

```json
{
    "type": "object",
    "properties": {
        "head": {
            "type": "integer",
            "description": "Number of people without safety helmets"
        },
        "helmet": {
            "type": "integer",
            "description": "Number of people with safety helmets"
        },
        "person": {
            "type": "integer",
            "description": "Total number of people in the image"
        },
        "alert": {
            "type": "boolean",
            "description": "Whether there are people without safety helmets"
        }
    },
    "required": ["head", "helmet", "person", "alert"]
}
``` 
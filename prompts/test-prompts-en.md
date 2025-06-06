# Safety Helmet Detection Prompt

## Detection Prompt

```prompt
Analyze whether the person in the image is wearing a safety helmet.

Steps to follow:
1. Carefully examine the head area of the person in the image
2. Look for the distinctive shape and color of a safety helmet
3. Consider the context (construction site, industrial area, etc.)

Guidelines for judgment:
- A proper safety helmet should cover the top of the head
- The helmet should be securely worn, not just held or placed nearby
- Hard hats in standard colors (yellow, white, blue, etc.) are safety helmets
- Regular caps, soft hats, or other non-protective headwear do NOT count as safety helmets

Return only a JSON in the following format without any explanation:
{
    "helmet": <whether the person is wearing a safety helmet, 1 means yes, 0 means no>
}
```

## Output Format Configuration

```json
{
    "type": "object",
    "properties": {
        "helmet": {
            "type": "integer",
            "enum": [0, 1],
            "description": "Whether the person is wearing a safety helmet (1=yes, 0=no)"
        }
    },
    "required": ["helmet"]
}
``` 
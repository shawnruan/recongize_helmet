# Safety Helmet Detection Prompt Configuration

## Basic Detection Prompt

```prompt
Determine whether the person in the image is wearing a safety helmet.
Only return JSON in the following format:
{
    "helmet": <whether wearing a safety helmet, 1 means wearing, 0 means not wearing>
}
```

## Output Format Configuration

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


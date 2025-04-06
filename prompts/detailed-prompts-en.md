# Detailed Safety Helmet Detection Prompt

## Detection Prompt

```prompt
Perform a detailed analysis of whether the person in the image is properly wearing a safety helmet.

Comprehensive analysis steps:
1. Carefully examine the entire person in the image, focusing on the head area
2. Identify the type of headwear (if any) the person is we\

aring
3. Determine if the headwear qualifies as a proper safety helmet
4. Check if the safety helmet is being worn correctly

Detailed guidelines for assessment:
- A proper safety helmet must:
  * Be made of hard, impact-resistant material
  * Cover the entire top and sides of the head
  * Have a harness or suspension system
  * Be specifically designed for protection
  * Be worn directly on the head (not on top of other headwear)

- The following are NOT considered safety helmets:
  * Regular hats, caps, or beanies
  * Decorative helmets not meant for safety
  * Sports helmets (unless in a relevant context)
  * Damaged or improperly worn safety helmets
  * Helmets held in hand or placed nearby but not worn

Evaluate the image against these criteria and return only a JSON in the following format without any explanation:
{
    "helmet": <whether the person is properly wearing a safety helmet, 1 means yes, 0 means no>
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
            "description": "Whether the person is properly wearing a safety helmet (1=yes, 0=no)"
        }
    },
    "required": ["helmet"]
}
``` 
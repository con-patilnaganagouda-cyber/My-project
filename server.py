#!/usr/bin/env python3
"""
Higgsfield MCP Server
Exposes image and video generation tools to Claude via the Model Context Protocol.
"""

import json
import re
from typing import Any

from dotenv import load_dotenv
load_dotenv()

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    CallToolResult,
)

from higgsfield_client import HiggsFieldClient, HiggsFieldError

app = Server("higgsfield-mcp")


def get_client() -> HiggsFieldClient:
    return HiggsFieldClient()


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    Tool(
        name="generate_image",
        description=(
            "Generate an image from a text prompt using Higgsfield AI. "
            "Returns a request_id for async polling, or the image URL if completed immediately."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Detailed description of the image to generate.",
                },
                "model": {
                    "type": "string",
                    "description": "Image model to use. Options: nano-banana-pro (4K), soul-2.0 (portraits), flux-2, seedream-5.0-lite, gpt-image-2.",
                    "default": "nano-banana-pro",
                },
                "negative_prompt": {
                    "type": "string",
                    "description": "Elements to avoid in the image.",
                    "default": "",
                },
                "seed": {
                    "type": "integer",
                    "description": "Seed for reproducible results (optional).",
                },
                "enhance_prompt": {
                    "type": "boolean",
                    "description": "Let Higgsfield enhance your prompt for better results.",
                    "default": True,
                },
                "wait": {
                    "type": "boolean",
                    "description": "Wait for completion and return the image URL directly (blocks up to 5 minutes).",
                    "default": False,
                },
            },
            "required": ["prompt"],
        },
    ),
    Tool(
        name="generate_video",
        description=(
            "Generate a video from a text prompt (text-to-video) using Higgsfield AI. "
            "Best for cinematic shots described in a screenplay."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Detailed cinematic description of the video scene.",
                },
                "model": {
                    "type": "string",
                    "description": "Video model. Options: seedance-2.0 (default), sora-2, kling-3.0, veo-3.1, wan-2.6, hailuo-02.",
                    "default": "seedance-2.0",
                },
                "duration": {
                    "type": "integer",
                    "description": "Video duration in seconds (typically 3-10).",
                    "default": 5,
                },
                "resolution": {
                    "type": "string",
                    "description": "Output resolution: 720p or 1080p.",
                    "default": "1080p",
                },
                "seed": {
                    "type": "integer",
                    "description": "Seed for reproducible results (optional).",
                },
                "enhance_prompt": {
                    "type": "boolean",
                    "description": "Let Higgsfield enhance your prompt for better results.",
                    "default": True,
                },
                "wait": {
                    "type": "boolean",
                    "description": "Wait for completion and return the video URL directly (blocks up to 5 minutes).",
                    "default": False,
                },
            },
            "required": ["prompt"],
        },
    ),
    Tool(
        name="image_to_video",
        description=(
            "Animate a still image into a video using Higgsfield AI (image-to-video). "
            "Provide an image URL and a motion description."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Description of the motion and action to apply to the image.",
                },
                "image_url": {
                    "type": "string",
                    "description": "Publicly accessible URL of the source image.",
                },
                "model": {
                    "type": "string",
                    "description": "Video model to use.",
                    "default": "seedance-2.0",
                },
                "duration": {
                    "type": "integer",
                    "description": "Video duration in seconds.",
                    "default": 5,
                },
                "camera_fixed": {
                    "type": "boolean",
                    "description": "Lock the camera position (no camera movement).",
                    "default": False,
                },
                "seed": {"type": "integer"},
                "wait": {
                    "type": "boolean",
                    "default": False,
                },
            },
            "required": ["prompt", "image_url"],
        },
    ),
    Tool(
        name="check_status",
        description="Check the status of a Higgsfield generation request by its request_id.",
        inputSchema={
            "type": "object",
            "properties": {
                "request_id": {
                    "type": "string",
                    "description": "The request_id returned by a generation call.",
                }
            },
            "required": ["request_id"],
        },
    ),
    Tool(
        name="get_result",
        description=(
            "Retrieve the completed result (image/video URLs) for a finished Higgsfield request."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "request_id": {
                    "type": "string",
                    "description": "The request_id of the completed generation.",
                }
            },
            "required": ["request_id"],
        },
    ),
    Tool(
        name="parse_screenplay",
        description=(
            "Parse a screenplay text and extract individual scenes with visual descriptions. "
            "Returns a structured list of scenes ready for image/video generation."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "screenplay": {
                    "type": "string",
                    "description": "Full screenplay text in standard format (INT./EXT. scene headings).",
                },
                "style": {
                    "type": "string",
                    "description": "Overall visual style to apply to all scenes (e.g. 'cinematic noir', 'vibrant anime', 'gritty realism').",
                    "default": "cinematic",
                },
            },
            "required": ["screenplay"],
        },
    ),
    Tool(
        name="generate_from_screenplay",
        description=(
            "Generate images OR videos for every scene in a screenplay. "
            "Parses the screenplay, builds a prompt for each scene, and submits all generation requests. "
            "Returns request_ids for all scenes."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "screenplay": {
                    "type": "string",
                    "description": "Full screenplay text.",
                },
                "mode": {
                    "type": "string",
                    "description": "What to generate per scene: 'image' or 'video'.",
                    "enum": ["image", "video"],
                    "default": "image",
                },
                "style": {
                    "type": "string",
                    "description": "Visual style to apply across all scenes.",
                    "default": "cinematic, high quality, film still",
                },
                "model": {
                    "type": "string",
                    "description": "Model to use for all generations.",
                    "default": "nano-banana-pro",
                },
                "direction": {
                    "type": "string",
                    "description": "Director's note / creative direction appended to every prompt.",
                    "default": "",
                },
            },
            "required": ["screenplay"],
        },
    ),
    Tool(
        name="cancel_request",
        description="Cancel a queued or in-progress Higgsfield generation request.",
        inputSchema={
            "type": "object",
            "properties": {
                "request_id": {"type": "string"}
            },
            "required": ["request_id"],
        },
    ),
]


# ---------------------------------------------------------------------------
# Screenplay parser
# ---------------------------------------------------------------------------

def parse_screenplay_scenes(screenplay: str, style: str = "cinematic") -> list[dict]:
    """Split a screenplay into scenes and build visual prompts."""
    # Match standard scene headings: INT. / EXT. / I/E.
    heading_pattern = re.compile(
        r"^((?:INT|EXT|I/E|INT\./EXT)[\.\s].+?)$",
        re.MULTILINE | re.IGNORECASE,
    )
    positions = [(m.start(), m.group(0).strip()) for m in heading_pattern.finditer(screenplay)]

    scenes = []
    for i, (start, heading) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(screenplay)
        body = screenplay[start:end].strip()

        # Remove heading from body, keep action lines (skip dialogue blocks)
        lines = body.splitlines()
        action_lines = []
        skip = False
        for line in lines[1:]:
            stripped = line.strip()
            # Skip character cues (all-caps short lines) and their dialogue
            if re.match(r"^[A-Z][A-Z\s\.\-']+$", stripped) and len(stripped) < 40:
                skip = True
                continue
            if skip and stripped.startswith("("):  # parenthetical
                continue
            if skip and stripped:
                skip = False  # resume after dialogue
            if stripped:
                action_lines.append(stripped)

        visual_description = " ".join(action_lines[:6])  # cap at 6 lines
        prompt = f"{style}, {heading}, {visual_description}".strip(", ")

        scenes.append({
            "scene_number": i + 1,
            "heading": heading,
            "prompt": prompt,
            "body_preview": visual_description[:200],
        })

    return scenes


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

@app.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent]:
    try:
        result = await _dispatch(name, arguments)
    except HiggsFieldError as e:
        return [TextContent(type="text", text=f"Higgsfield error: {e}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {e}")]

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _dispatch(name: str, args: dict) -> Any:
    client = get_client()
    wait = args.get("wait", False)

    if name == "generate_image":
        resp = client.generate_image(
            prompt=args["prompt"],
            model=args.get("model", "nano-banana-pro"),
            negative_prompt=args.get("negative_prompt", ""),
            seed=args.get("seed"),
            enhance_prompt=args.get("enhance_prompt", True),
        )
        if wait:
            rid = resp.get("request_id") or resp.get("generation_id")
            return client.wait_for_completion(rid)
        return resp

    elif name == "generate_video":
        resp = client.generate_video(
            prompt=args["prompt"],
            model=args.get("model", "seedance-2.0"),
            duration=args.get("duration", 5),
            resolution=args.get("resolution", "1080p"),
            seed=args.get("seed"),
            enhance_prompt=args.get("enhance_prompt", True),
        )
        if wait:
            rid = resp.get("request_id") or resp.get("generation_id")
            return client.wait_for_completion(rid)
        return resp

    elif name == "image_to_video":
        resp = client.image_to_video(
            prompt=args["prompt"],
            image_url=args["image_url"],
            model=args.get("model", "seedance-2.0"),
            duration=args.get("duration", 5),
            camera_fixed=args.get("camera_fixed", False),
            seed=args.get("seed"),
        )
        if wait:
            rid = resp.get("request_id") or resp.get("generation_id")
            return client.wait_for_completion(rid)
        return resp

    elif name == "check_status":
        return client.get_status(args["request_id"])

    elif name == "get_result":
        return client.get_result(args["request_id"])

    elif name == "cancel_request":
        return client.cancel(args["request_id"])

    elif name == "parse_screenplay":
        scenes = parse_screenplay_scenes(
            args["screenplay"],
            style=args.get("style", "cinematic"),
        )
        return {"total_scenes": len(scenes), "scenes": scenes}

    elif name == "generate_from_screenplay":
        screenplay = args["screenplay"]
        mode = args.get("mode", "image")
        style = args.get("style", "cinematic, high quality, film still")
        model = args.get("model", "nano-banana-pro" if mode == "image" else "seedance-2.0")
        direction = args.get("direction", "")

        scenes = parse_screenplay_scenes(screenplay, style=style)
        results = []

        for scene in scenes:
            prompt = scene["prompt"]
            if direction:
                prompt = f"{prompt}. Director's note: {direction}"

            if mode == "image":
                resp = client.generate_image(prompt=prompt, model=model)
            else:
                resp = client.generate_video(prompt=prompt, model=model)

            rid = resp.get("request_id") or resp.get("generation_id", "unknown")
            results.append({
                "scene_number": scene["scene_number"],
                "heading": scene["heading"],
                "prompt": prompt,
                "request_id": rid,
                "status": resp.get("status", "submitted"),
            })

        return {
            "mode": mode,
            "total_scenes": len(results),
            "generations": results,
            "tip": "Use check_status or get_result with each request_id to retrieve results.",
        }

    else:
        raise ValueError(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

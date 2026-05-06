#!/usr/bin/env python3
"""
MVS 2.0 — Scene 2 Image Generator
Generates all 42 shots for INT. HIGH SCHOOL — GYMNASIUM — DAY
Model: nano-banana-pro | Aspect ratio: 1:1
Run this on YOUR LOCAL MACHINE (not in cloud).

Usage:
    pip install httpx python-dotenv
    export HF_API_KEY=your_key   # or put in .env
    python generate_scene2.py
"""

import json
import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("HF_API_KEY") or os.environ.get("HF_KEY")
BASE_URL = "https://platform.higgsfield.ai"
MODEL = "nano-banana-pro"
ASPECT_RATIO = "1:1"
RESULTS_FILE = "scene2_results.json"

# ---------------------------------------------------------------------------
# Shot list — all 42 images
# ---------------------------------------------------------------------------

LOCATION_MASTER = (
    "Large high school gymnasium interior — polished hardwood floor with faded basketball "
    "court line markings, high industrial ceiling with exposed metal beams, harsh overhead "
    "fluorescent strip lighting casting cool blue-white downward shadows, tall narrow windows "
    "along one wall with cold daylight bleeding in. Cool blue-green desaturated color grade. "
    "High cinematic contrast. 35mm film grain. Sam Raimi Spider-Man + Zack Snyder Man of Steel visual style."
)

QUINN_DESC = (
    "Quinn: 18-year-old Caucasian male, lean slightly athletic build, tousled dark brown hair, "
    "fitted black round-neck t-shirt slightly torn and rumpled, dark tailored trousers, white "
    "low-profile sneakers, thin round metal-frame glasses, black Apple Watch on wrist. "
    "Dried blood beneath nose, slight abrasion on knuckle, icicle cut on forearm."
)

RYLIE_DESC = (
    "Rylie: 18-year-old Caucasian male, tall muscular build, sky-blue short-sleeve hoodie, "
    "muted yellow undershirt visible at collar, light grey denim jeans, red-and-white Converse "
    "sneakers, curly ginger hair, flame tattoos on forearms, black Apple Watch."
)

DEL_DESC = (
    "Mister Del: man in his late 40s, charcoal tailored blazer, structured shoulders, short "
    "slightly greying light brown hair, round black thin-frame eyeglasses, sharp gaunt features, "
    "light stubble, cold authoritative expression."
)

SHOTS = [
    {
        "id": "2.1",
        "label": "WIDE ESTABLISHING SHOT — LOW ANGLE",
        "prompt": (
            "Cinematic still, wide establishing shot, "
            + LOCATION_MASTER
            + " Dozens of 17-18-year-old students in neat school uniforms — fitted blazers, dark trousers — "
            "engaged in violent supernatural combat across the full gymnasium floor. Left frame: a student "
            "encased in blue ice armor launches ice shards. Center: two students exchange crackling golden "
            "lightning bolts, electricity arcing across the floor. Right frame: a student levitates two "
            "feet off the ground, wind blasting radially outward. Frost mist and holographic energy debris "
            "float in the air. Camera LOW ANGLE — one foot off gym floor, shooting upward toward the chaos. "
            "Ceiling beams and fluorescent lights tower above. Slight 10-degree dutch tilt. No main "
            "characters in frame. Ultra-photorealistic. IMAX-quality clarity."
        ),
    },
    {
        "id": "2.2",
        "label": "MEDIUM WIDE — DUTCH ANGLE 15° — THREE COMBAT STUDENTS",
        "prompt": (
            "Cinematic still, medium wide shot, "
            + LOCATION_MASTER
            + " Three superpowered students mid-combat: LEFT — 18-year-old male, blue-white crystalline "
            "ice armor coating arms and torso, launching a thick ice shard forward. CENTER — 17-year-old "
            "female, body surrounded by crackling golden electricity, arms raised, lightning arcing from "
            "fingertips. RIGHT — 18-year-old male levitating two feet off gym floor, wind visibly warping "
            "around him, hair and uniform blown upward. Camera medium wide, chest to foot, 15-degree dutch "
            "tilt. Eye-level inside the chaos. Electricity glow adding warm amber bounce. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.3",
        "label": "INSERT — EXTREME CLOSE UP — LIGHTNING STRIKE FLOOR",
        "prompt": (
            "Cinematic still, extreme close-up insert, "
            + LOCATION_MASTER
            + " A bolt of lightning striking the polished hardwood gymnasium floor — sparks and char "
            "fragments scattering radially outward across court line markings. Wood scorches and splinters "
            "at impact point. Smoke rising. Surrounding floor reflects warm amber flash. Camera floor-level, "
            "tilted slightly upward. Very shallow depth of field — sparks sharp in center, edges bokeh blur. "
            "Intense warm amber flash on floor, cool fluorescent ambient from above. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.4",
        "label": "OVER-THE-SHOULDER — QUINN'S POV — WIDE INTO BATTLEFIELD",
        "prompt": (
            "Cinematic still, over-the-shoulder wide shot, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn visible from behind, slightly left — posture braced, shoulders up, arms slightly "
            "raised defensively. Beyond him, gymnasium erupts in chaos — ice flying left, lightning "
            "crackling right, students battling across full floor. He looks small against it. Isolated. "
            "Determined. Camera over-the-shoulder from just behind Quinn's right shoulder, wide framing, "
            "LOW ANGLE — Quinn feels brave stepping into the impossible. Cool fluorescent overhead, "
            "Quinn's back in slight silhouette against the chaos ahead. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.5",
        "label": "CLOSE UP — QUINN'S FACE — DETERMINED",
        "prompt": (
            "Cinematic still, close-up portrait, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Expression: jaw set tight, eyes burning with quiet determination despite fear. Lips pressed "
            "together. Breathing controlled. Slightly vulnerable but not broken. Camera close-up, eye-level, "
            "direct gaze slightly off-camera. Shallow depth of field — Quinn sharp, gymnasium chaos softly "
            "blurred. Harsh cool fluorescent from above, strong top-down shadow beneath brow, cheekbones "
            "catch overhead light, chin drops into shadow. Visible skin pores, subtle stubble, realistic "
            "glasses lens reflection. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.6",
        "label": "INSERT — EXTREME CLOSE UP — QUINN'S HAND ON DOOR FRAME",
        "prompt": (
            "Cinematic still, extreme close-up insert, "
            + LOCATION_MASTER
            + " Quinn's hand gripping a gymnasium door frame — 18-year-old male hand, lean fingers, "
            "knuckles whitened from grip pressure. Slight abrasion on knuckle. Black Apple Watch at wrist. "
            "Metal door frame edge catches cold fluorescent highlight. Deep shadow in grip creases. "
            "Extreme close-up, slightly angled. Shallow depth of field. Gymnasium chaos softly blurred behind. "
            "Ultra-photorealistic."
        ),
    },
    {
        "id": "2.7",
        "label": "WIDE SHOT — LOW ANGLE — QUINN CHARGING IN",
        "prompt": (
            "Cinematic still, wide shot, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn mid-stride, running hard into the gymnasium mid-battle, both arms raised in X-guard "
            "across face to block an incoming wind blast from the left. T-shirt and hair whip violently "
            "to the right from wind force. Students around him pause mid-combat to look at the intruder. "
            "Ice shards fly across frame. Lightning crackles in background. Camera LOW ANGLE, wide framing, "
            "approximately two feet off gym floor, shooting slightly upward. Quinn is focus, battlefield "
            "chaos fills background. Kinetic war-film energy. Dynamic motion framing. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.8",
        "label": "MEDIUM SHOT — DUTCH ANGLE 20° — QUINN BRACING WIND",
        "prompt": (
            "Cinematic still, medium shot, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn bracing hard against a wind blast — t-shirt whipping violently, glasses slightly "
            "pushed sideways by wind force, one hand reaching up to stabilize them. Hair blown flat against "
            "forehead. Eyes squinting against the force. Feet planted. Body leaning at angle against the blast. "
            "Camera medium shot head to hip, 20-degree dutch tilt, slightly low angle. Maximum tension, "
            "physical struggle, instability. Air distortion visible in atmosphere. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.9",
        "label": "OVER-THE-SHOULDER — MISTER DEL'S POV — WIDE ON QUINN",
        "prompt": (
            "Cinematic still, over-the-shoulder wide shot, "
            + LOCATION_MASTER
            + " " + DEL_DESC + " " + QUINN_DESC
            + " Mister Del visible from behind in foreground — charcoal blazer, slightly greying hair, "
            "authoritative posture, arms crossed. Across the gymnasium floor — students fighting, ice "
            "lightning wind filling the space — Quinn visible in far distance at gymnasium entrance. "
            "Small. Alone. An intruder. The BLACK ABILITY BOOK visible on gymnasium floor near Del's feet, "
            "faint barely perceptible crimson glow. Camera over-the-shoulder from Del's right shoulder, "
            "wide framing, deep depth of field — both Del and Quinn sharp. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.10",
        "label": "MEDIUM CLOSE-UP — LOW ANGLE — MISTER DEL TOWERING",
        "prompt": (
            "Cinematic still, medium close-up, "
            + LOCATION_MASTER
            + " " + DEL_DESC
            + " Expression: cold, contemptuous, utterly unmoved. Arms crossed. Camera LOW ANGLE — shooting "
            "upward from Quinn's eye level. Del appears towering, authoritative, superior. He looks DOWN "
            "at the camera. Shallow depth of field — Del sharp, gymnasium chaos blurred behind. Harsh "
            "overhead fluorescent from above — deep top-down shadow beneath brow, cheekbones catch the "
            "overhead light. Glasses lenses catch sharp fluorescent strip reflection. Slightly backlit "
            "from gymnasium windows — subtle silhouette authority. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.11",
        "label": "LOW ANGLE CLOSE-UP — DEL LOOKING DIRECTLY DOWN",
        "prompt": (
            "Cinematic still, low angle close-up, "
            + LOCATION_MASTER
            + " " + DEL_DESC
            + " Shot from directly below looking upward — cold, contemptuous, superior. Round black "
            "eyeglasses. Sharp angular features. Short greying hair above. Fluorescent ceiling strip "
            "lights visible behind his head like a cold halo. Expression: sneering disgust. He is looking "
            "directly DOWN at the camera. Camera extreme low angle, shooting straight up. Del's face fills "
            "upper frame, fluorescent lights and ceiling beams visible behind him. Very dramatic top-down "
            "shadow across upper face. Deeply intimidating perspective. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.12",
        "label": "INSERT — EXTREME CLOSE UP — THE BLACK ABILITY BOOK",
        "prompt": (
            "Cinematic still, extreme close-up insert, "
            + LOCATION_MASTER
            + " THE BLACK ABILITY BOOK lying on polished hardwood gymnasium floor — a medium-thick "
            "hard-cover ancient book, deep dark-red leather surface, rich aged crimson tone with natural "
            "wear, cracked and weathered. Cover design: deeply engraved circular ritual ring with ancient "
            "symbols. Central structure: grotesque mouth-like cavity with protruding aged ivory-yellow "
            "vampire fangs. Engravings emit barely perceptible dim crimson glow — faint, subtle, barely "
            "visible like a whisper. Dust around the book on gymnasium floor. Camera floor-level, "
            "shallow depth of field — book sharp, surrounding floor and feet blurred. Cool overhead "
            "fluorescent with book's own faint internal crimson glow. Ultra-photorealistic detailed "
            "leather grain, cracks, realistic tooth texture."
        ),
    },
    {
        "id": "2.13",
        "label": "MEDIUM SHOT — MISTER DEL SPEAKING — LECTURING",
        "prompt": (
            "Cinematic still, medium shot, "
            + LOCATION_MASTER
            + " " + DEL_DESC
            + " Cold lecture energy — lips parted mid-sentence, eyes fixed on Quinn off-camera with "
            "contempt. Arms crossed, one arm slightly gesturing dismissively. Students behind him have "
            "paused mid-combat to watch. Gymnasium background visible — frost mist, students in various "
            "combat stances all now observing. Camera medium shot head to hip, eye-level, Del centered, "
            "slightly low angle to reinforce authority. Harsh overhead fluorescent. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.14",
        "label": "OVER-THE-SHOULDER — DEL'S POV — HIGH ANGLE DOWN ON QUINN",
        "prompt": (
            "Cinematic still, over-the-shoulder shot, "
            + LOCATION_MASTER
            + " " + DEL_DESC + " " + QUINN_DESC
            + " From behind Mister Del, HIGH ANGLE looking DOWN across gymnasium floor at Quinn standing "
            "in the distance, alone, surrounded by hostile students who stare. Del visible from behind "
            "in foreground — charcoal blazer, dominant, close, left of screen. Quinn visible in "
            "mid-distance — lean build, black t-shirt rumpled, thin round glasses, posture tense but "
            "trying not to show vulnerability. He looks small. Isolated. A dozen students staring "
            "judgmentally. Camera over-the-shoulder from Del's right shoulder, HIGH ANGLE looking down. "
            "Quinn appears small, diminished, powerless. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.15",
        "label": "CLOSE UP — QUINN ABSORBING DEL'S WORDS",
        "prompt": (
            "Cinematic still, close-up, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Expression: pain layered beneath controlled anger. Jaw tight, eyes slightly glistening "
            "(not crying — barely holding it), lips pressed firmly together. But beneath the humiliation — "
            "fire. Eyes flicking momentarily downward toward the book, then back up. Camera close-up, "
            "eye-level. Shallow depth of field. Background gymnasium softly blurred. Harsh overhead "
            "fluorescent. Top-down shadow dramatic across brow. Emotional close-up framing. Visible skin "
            "pores, realistic glasses, natural eye moisture. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.16",
        "label": "WIDE SHOT — DUTCH 25° — QUINN SURROUNDED AS TARGET",
        "prompt": (
            "Cinematic still, wide shot, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn standing at center of gymnasium, completely surrounded by superpowered students in "
            "school uniforms using him as a target. Left: a student launches a small rock with telekinesis. "
            "Right: another fires a wind pulse. Behind Quinn: a student casually ignites a small flame "
            "toward him. Quinn at center frame, visibly braced, defensive, overwhelmed. Camera wide framing, "
            "25-degree dutch tilt. Low angle — surrounding students feel imposing. Multiple student power "
            "glow effects adding warm and cold bounce light from various directions. Chaotic lighting. "
            "Ultra-photorealistic."
        ),
    },
    {
        "id": "2.17",
        "label": "MEDIUM SHOT — FREEZE FRAME — ROCK MID-AIR AT QUINN",
        "prompt": (
            "Cinematic still, medium shot, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " A grey rock frozen mid-air, inches from Quinn's stomach. Quinn's face slightly turned "
            "away, eyes wincing, bracing for the impact he hasn't been able to dodge. Arms half-raised "
            "too late. T-shirt slightly rippled from prior wind blast. The rock sharp-focused, captured "
            "in slow-motion freeze-frame energy. Background students blurred — watching, indifferent. "
            "Camera medium shot head to hip, eye-level. Rock sharp in center, everything else slightly "
            "motion-blurred to suggest fast action frozen. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.18",
        "label": "CLOSE UP — QUINN DOUBLED OVER FROM ROCK IMPACT",
        "prompt": (
            "Cinematic still, close-up, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn doubled forward after rock impact — one hand pressed to stomach, face grimacing in "
            "pain, glasses slightly jostled sideways. Tousled hair falling forward over forehead. Eyes "
            "squeezed partially shut. Jaw clenched. Breathing sharp. Vulnerable but something in his "
            "expression hasn't broken. A quiet fire beneath the pain. Camera close-up, slightly elevated "
            "angle looking down at him as he bends. Deep top-down shadow across doubled frame. "
            "Ultra-photorealistic."
        ),
    },
    {
        "id": "2.19",
        "label": "EXTREME CLOSE UP — ICICLE SLICING QUINN'S FOREARM",
        "prompt": (
            "Cinematic still, extreme close-up, "
            + LOCATION_MASTER
            + " A sharp icicle slicing across Quinn's forearm in slow-motion freeze-frame — the ice shard "
            "mid-contact, splitting and shattering on impact. A clean cut appears on skin, blood beginning "
            "to emerge in a thin line. Ice fragments scatter in air around the contact point. Visible skin "
            "pores, fine arm hair, realistic wound detail. Black Apple Watch visible at wrist just above "
            "impact zone. Camera extreme close-up, slightly angled. Shallow depth of field. Cool overhead "
            "fluorescent, cold translucent blue-white refraction from ice shard. Ultra-photorealistic — "
            "real wound, real ice texture, real skin."
        ),
    },
    {
        "id": "2.20",
        "label": "INSERT — BLOOD TRICKLING DOWN QUINN'S ARM",
        "prompt": (
            "Cinematic still, extreme close-up insert, "
            + LOCATION_MASTER
            + " Blood trickling down Quinn's forearm — a thin red line running down pale skin from icicle "
            "cut. Blood catches cold fluorescent light above, appearing vivid crimson against cool-toned "
            "skin. Dripping toward gymnasium hardwood floor below. Visceral. Real. Below frame: polished "
            "gym floor with first drop of blood landing on wood grain. Camera extreme close-up, vertical "
            "orientation. Cool overhead fluorescent. The blood is the warm focal point in a cold frame. "
            "Ultra-photorealistic."
        ),
    },
    {
        "id": "2.21",
        "label": "CLOSE UP — QUINN'S EYES — RAGE RISING",
        "prompt": (
            "Cinematic still, close-up, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn's eyes and upper face — hazel-brown eyes behind thin round metal-frame glasses, "
            "dark tousled hair, dried and now fresh blood visible on face. His eyes snap to his arm then "
            "rise again — pain transforming into controlled rage. The fear is still there but underneath "
            "something harder has been activated. Dutch angle slight 10 degrees. His breaking point "
            "approaching. Camera close-up, eye-level. Eyes are the focus. Shallow depth of field. Harsh "
            "overhead fluorescent. Hard top-down brow shadow. Eyes catch sharp specular highlight. "
            "Ultra-photorealistic."
        ),
    },
    {
        "id": "2.22",
        "label": "WIDE SHOT — THE RACE FOR THE BOOK — QUINN DIVING",
        "prompt": (
            "Cinematic still, wide shot, "
            + LOCATION_MASTER
            + " " + QUINN_DESC + " " + RYLIE_DESC
            + " Quinn diving across the gymnasium floor reaching for THE BLACK ABILITY BOOK — full dive, "
            "body horizontal, arm fully extended reaching for the book. Hair and clothes in motion. "
            "Desperate. Rylie's arm entering frame from the right simultaneously — extending downward "
            "toward the book with casual athletic speed and dominance. THE BOOK on polished hardwood "
            "floor between them. Camera wide shot, low angle approximately one foot off gym floor. Both "
            "characters sharp, battlefield background softly blurred. Who gets there first? "
            "Ultra-photorealistic."
        ),
    },
    {
        "id": "2.23",
        "label": "EXTREME CLOSE UP — TWO HANDS REACHING FOR THE BOOK",
        "prompt": (
            "Cinematic still, extreme close-up, "
            + LOCATION_MASTER
            + " Two hands reaching for THE BLACK ABILITY BOOK simultaneously — Rylie's large muscular hand "
            "(visible flame tattoo on forearm, ginger arm hair) closing around the dark red leather book "
            "cover, Quinn's lean fingers arriving a fraction of a second later, fingertips brushing the "
            "spine just as Rylie's grip secures it. Quinn's hand can't close. Heartbreaking proximity — "
            "millimeters from reaching it. The book's ancient engraved symbols faintly visible under both "
            "hands. Camera extreme close-up, floor-level angle, both hands and book sharp. Shallow depth "
            "of field. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.24",
        "label": "LOW ANGLE CLOSE UP — RYLIE TRIUMPHANT OVER QUINN",
        "prompt": (
            "Cinematic still, low angle close-up, "
            + LOCATION_MASTER
            + " " + QUINN_DESC + " " + RYLIE_DESC
            + " Rylie standing, book held high, looking down with cold contempt at Quinn on the floor "
            "below. Rylie holding THE BLACK ABILITY BOOK up above Quinn, casual dominance, faint smirk "
            "of cold satisfaction. Backlit from gymnasium windows behind him — outline sharp against "
            "cool window light, slight silhouette aura. Quinn visible at very bottom of frame on "
            "gymnasium floor — lean build, glasses askew, reaching arm just lowering in defeat, "
            "looking up at Rylie. Camera LOW ANGLE shooting upward from Quinn's floor-level perspective. "
            "Rylie towers above, book held high. Dominant, imposing. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.25",
        "label": "MEDIUM SHOT — RYLIE SWINGING THE BOOK AS WEAPON",
        "prompt": (
            "Cinematic still, medium shot, "
            + LOCATION_MASTER
            + " " + RYLIE_DESC
            + " Rylie mid-swing — swinging THE BLACK ABILITY BOOK as a weapon toward the left of frame "
            "where Quinn stands. The book is motion-blurred — extreme velocity. Rylie's expression: cold "
            "contemptuous fury, enjoying this. Muscular arm extended in arc of swing. Flame tattoos catch "
            "overhead light. Camera medium shot head to hip, eye-level. Book in sharp motion blur — speed "
            "and violence communicated. Background blurred. Harsh overhead fluorescent. Cold. "
            "Ultra-photorealistic."
        ),
    },
    {
        "id": "2.26",
        "label": "EXTREME CLOSE UP — BOOK IMPACT ON QUINN'S FACE",
        "prompt": (
            "Cinematic still, extreme close-up, "
            + LOCATION_MASTER
            + " THE BLACK ABILITY BOOK connecting with Quinn's face — book cover sharp against Quinn's "
            "cheek and nose at point of impact. Sweat droplets scattering in slow-motion freeze-frame. "
            "Blood launching from his nose on impact — vivid crimson drops suspended mid-air. Quinn's "
            "glasses momentarily dislodged slightly. The book's ancient symbols and leather texture in "
            "extreme detail at point of impact. Camera extreme close-up, 25-degree dutch tilt. Maximum "
            "impact energy. Freeze-frame violence. Cold overhead fluorescent. Blood droplets are the "
            "warm focal point. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.27",
        "label": "INSERT — QUINN'S BLOOD ON BOOK COVER — FORESHADOWING",
        "prompt": (
            "Cinematic still, extreme close-up insert, "
            + LOCATION_MASTER
            + " THE BLACK ABILITY BOOK cover — dark red aged leather, ancient circular engravings, "
            "vampire fang mouth cavity — with Quinn's BLOOD landing on the cover. Several crimson droplets "
            "have struck the book, landing directly on ancient engravings and circular symbols. One droplet "
            "sits centered on the engraved ring. The blood is vivid against dark leather. Beneath the blood "
            "droplets — the engravings begin to emit the faintest possible crimson internal glow — barely "
            "visible, like the faintest ember. Foreshadowing everything. Camera extreme close-up, "
            "floor-level angle. Shallow depth of field. Cold overhead fluorescent. Book's faint internal "
            "glow is the only warm source. Ultra-photorealistic — realistic leather grain, blood texture."
        ),
    },
    {
        "id": "2.28",
        "label": "WIDE SHOT — GYMNASIUM FREEZES AT BELL",
        "prompt": (
            "Cinematic still, wide shot, "
            + LOCATION_MASTER
            + " " + QUINN_DESC + " " + RYLIE_DESC + " " + DEL_DESC
            + " The gymnasium frozen mid-chaos — every student stopped simultaneously as the school bell "
            "rings. Ice shards hang in mid-air suspended. Lightning mid-arc. Wind dropped. Every student "
            "completely still, mid-combat. Quinn on gymnasium floor at center — lean build, black t-shirt, "
            "glasses askew, bleeding from nose, arm bloodied, looking up with relief beneath humiliation. "
            "Rylie standing over him — tall, muscular, ginger hair, sky-blue hoodie, book in hand. Stopped. "
            "Mister Del in background — charcoal blazer, arms crossed, utterly unmoved. All students "
            "staring at Quinn on the floor. Camera wide shot, slightly LOW ANGLE. Overhead fluorescent "
            "throughout. Static. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.29",
        "label": "INSERT — GYMNASIUM BELL ON WALL",
        "prompt": (
            "Cinematic still, close-up insert, "
            + LOCATION_MASTER
            + " Old institutional school bell mounted on the gymnasium wall — metal bell, mounted on "
            "painted cinder block wall beside the bleachers. The bell mid-ring. Motion blur on the bell "
            "mechanism. Cold institutional lighting. Mundane and real. The most ordinary thing in an "
            "extraordinary scene. Camera close-up, straight on. Gymnasium bleachers and wall in background. "
            "Cool overhead fluorescent. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.30",
        "label": "MEDIUM SHOT — QUINN ON FLOOR — EVERYONE STARING",
        "prompt": (
            "Cinematic still, medium shot, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn sitting on the gymnasium floor — chest rising and falling, glasses slightly crooked, "
            "fresh blood on face and arm. He looks up at a ring of students staring down at him. Expression: "
            "trying to maintain composure under the humiliation. He clutches his left arm where the icicle "
            "cut him. Students visible at edges of frame — school uniforms, power residue effects "
            "dissipating. All eyes on Quinn. Camera medium shot, slightly HIGH ANGLE looking down at "
            "Quinn on the floor. Students visible standing around frame edges. Overhead fluorescent. "
            "Top-down. Cold. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.31",
        "label": "MEDIUM SHOT — DEL AND RYLIE — APPROVING PAT",
        "prompt": (
            "Cinematic still, medium shot, "
            + LOCATION_MASTER
            + " " + DEL_DESC + " " + RYLIE_DESC
            + " Mister Del with one hand on Rylie's shoulder — quiet, approving, complicit. Del's "
            "expression: cold satisfaction. Rylie receiving the approval with casual arrogance, a slight "
            "satisfied smirk. THE BLACK ABILITY BOOK tucked under Del's other arm, held casually. Faint "
            "ambient gymnasium background. Camera medium shot head to hip, eye-level. Both characters in "
            "frame, Del slightly closer. Overhead fluorescent. Cold. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.32",
        "label": "CLOSE UP — DEL'S HANDS HOLDING THE BOOK — CRIMSON GLOW",
        "prompt": (
            "Cinematic still, close-up, "
            + LOCATION_MASTER
            + " Mister Del's hands holding THE BLACK ABILITY BOOK — aged hands in their late 40s, wearing "
            "charcoal blazer sleeve. The book's dark red leather cover faces outward. From the ancient "
            "circular engravings, a soft dim crimson glow bleeds onto Del's fingers and palm — subtle, "
            "warm, alive. Del doesn't notice it. His grip is casual. But the book is responding to something. "
            "Camera close-up, slightly angled. Medium depth of field — hands and book sharp, Del's body "
            "softly blurred above. Cool overhead fluorescent ambient, the book's own internal crimson glow "
            "as primary warm fill on hands. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.33",
        "label": "EXTREME CLOSE UP — BOOK ENGRAVINGS GLOWING CRIMSON",
        "prompt": (
            "Cinematic still, extreme close-up, "
            + LOCATION_MASTER
            + " THE BLACK ABILITY BOOK cover — the ancient circular ritual ring engravings glowing dim "
            "crimson from within. The glow is subtle — not dramatic, not bright. The kind of glow you'd "
            "almost miss. Like a dying ember just catching. The leather around the engravings absorbs the "
            "light slightly. The vampire fang mouth cavity at center catches the internal warmth. Ancient. "
            "Dangerous. Awakening. Camera extreme close-up, tilted slightly. Shallow depth of field. The "
            "glow is entirely self-generated — dim warm crimson in a cold ambient environment. "
            "Ultra-photorealistic — realistic leather grain, subtle glow precisely grounded."
        ),
    },
    {
        "id": "2.34",
        "label": "MEDIUM CLOSE UP — MISTER DEL SNEERING AT QUINN",
        "prompt": (
            "Cinematic still, medium close-up, "
            + LOCATION_MASTER
            + " " + DEL_DESC
            + " Looking down at Quinn with cold contempt. Lips curled slightly in a sneer as he speaks. "
            "Eyes analytical and dismissive. Students visible behind him — watching silently, some faintly "
            "amused. Camera medium close-up, slightly LOW ANGLE — Del slightly above eye line, reinforcing "
            "authority. Shallow depth of field. Overhead fluorescent. Hard top-down shadow on Del's "
            "features. Cold. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.35",
        "label": "CLOSE UP — QUINN ABSORBING 'JUST LIKE YOUR PARENTS'",
        "prompt": (
            "Cinematic still, close-up, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn's face as Del's words land — hazel-brown eyes behind thin round metal-frame glasses. "
            "Expression: jaw tightening. Eyes glistening slightly — not crying, the opposite. Something "
            "cementing. Humiliation becoming resolve. The flicker of a young man deciding something in "
            "real time. Camera close-up, eye-level. Shallow depth of field — face sharp, gymnasium "
            "background pure blur. Harsh overhead fluorescent, top-down dramatic shadow. High contrast "
            "on face. Visible skin pores, realistic moisture in eyes. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.36",
        "label": "OVER-THE-SHOULDER — QUINN'S POV HIGH ANGLE — DEL TOWERS",
        "prompt": (
            "Cinematic still, over-the-shoulder shot, "
            + LOCATION_MASTER
            + " " + DEL_DESC + " " + QUINN_DESC
            + " From just behind and below Quinn looking up at Mister Del — HIGH ANGLE on Quinn, LOW ANGLE "
            "of Del. Quinn visible from behind — smaller, lower, sitting or crouching. Del fills the frame "
            "above, looming. Students behind Del all staring downward at Quinn. Gymnasium ceiling behind "
            "Del with fluorescent strips creating a cold institutional halo above him. Camera "
            "over-the-shoulder, HIGH ANGLE on Quinn, Del towers above. The entire gymnasium presses down "
            "on Quinn from this angle. Overhead fluorescent throughout. Cold blue-white. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.37",
        "label": "EXTREME CLOSE UP — QUINN'S EYES — THE HIT LANDS",
        "prompt": (
            "Cinematic still, extreme close-up, "
            + LOCATION_MASTER
            + " Quinn's eyes — hazel-brown, behind thin round metal-frame glasses. The moment Del says "
            "'just like your parents' — something shifts visibly. The eyes go still. Fear disappears. "
            "Something harder and deeper replaces it. Not anger — grief, transmuted instantly into iron "
            "will. Eyes slightly wider, then settling into absolute focus. A decision being made behind them. "
            "Camera extreme close-up, eyes only — glasses, eyebrows, bridge of nose. Nothing else. Shallow "
            "depth of field. Overhead fluorescent, hard specular highlight in each eye. Deep shadow above "
            "from brows. Individual iris detail, realistic glasses lens. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.38",
        "label": "MEDIUM SHOT — DEL WALKING AWAY — QUINN SMALL BEHIND",
        "prompt": (
            "Cinematic still, medium shot, "
            + LOCATION_MASTER
            + " " + DEL_DESC + " " + QUINN_DESC
            + " Mister Del walking away from camera, back turned, charcoal blazer, composed posture, "
            "completely dismissive. He does not look back. Quinn visible in the background — sitting on "
            "the gymnasium floor, small, alone, students around him beginning to disperse. The distance "
            "between Del and Quinn feels enormous. Camera medium shot, slightly behind Del as he walks "
            "away. Quinn visible in far background. Eye-level. The composition says everything — Del's "
            "back, Quinn's isolation. Overhead fluorescent throughout. Cold. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.39",
        "label": "INSERT — QUINN'S BLOODY HAND REACHING FOR THE BOOK",
        "prompt": (
            "Cinematic still, extreme close-up insert, "
            + LOCATION_MASTER
            + " Quinn's bloody hand slowly reaching across the gymnasium floor toward THE BLACK ABILITY "
            "BOOK — Del has just tossed it back. Quinn's lean fingers, slightly trembling, blood on the "
            "back of his hand and forearm from the icicle cut, stretching toward the book. His fingers "
            "beginning to close around the dark red leather spine. Claiming it. Not giving up. Camera "
            "extreme close-up, floor-level. Quinn's hand and book sharp. Gymnasium floor grain visible "
            "in detail. Overhead fluorescent cold ambient. Blood catches faint warm contrast. "
            "Ultra-photorealistic."
        ),
    },
    {
        "id": "2.40",
        "label": "WIDE SHOT — BIRD'S EYE — QUINN ALONE WITH BOOK",
        "prompt": (
            "Cinematic still, wide shot, bird's eye view directly overhead, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Looking straight down at gymnasium floor. Quinn sits at the center of frame on polished "
            "hardwood floor, THE BLACK ABILITY BOOK clutched to his chest with both arms. Around him in "
            "a loose ring: students in school uniforms, some laughing, some pointing, some turning away. "
            "Quinn perfectly centered — completely alone in the center of the frame. The basketball court "
            "circle line beneath him frames him like a spotlight. Isolated. Surrounded. But not defeated. "
            "Camera bird's eye directly overhead. Wide framing — Quinn small at center, students filling "
            "the ring. Overhead fluorescent straight down. Perfect top-down light. Quinn's shadow directly "
            "beneath him. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.41",
        "label": "CLOSE UP — QUINN'S FACE — TUNED OUT — STARING AT BOOK",
        "prompt": (
            "Cinematic still, close-up, "
            + LOCATION_MASTER
            + " " + QUINN_DESC
            + " Quinn's face — hazel-brown eyes behind thin round metal-frame glasses, tousled dark brown "
            "hair, blood on his face. His eyes are completely fixed on THE BOOK clutched in his arms just "
            "below frame. He is not hearing the laughter. Completely tuned out. The world behind him is "
            "blurred — laughing students visible but soft, irrelevant. It is just him and the book. "
            "Tunnel vision has begun. Obsession is starting. Camera close-up, eye-level. His face sharp, "
            "book visible at lower frame edge, everything behind deeply blurred. Shallow depth of field. "
            "Overhead fluorescent. Hard top-down shadow. Eyes are the focal point. Ultra-photorealistic."
        ),
    },
    {
        "id": "2.42",
        "label": "EXTREME CLOSE UP — QUINN'S EYES REFLECTING BOOK'S CRIMSON GLOW",
        "prompt": (
            "Cinematic still, extreme close-up, "
            + LOCATION_MASTER
            + " Quinn's eyes reflected with the book's faint crimson glow — hazel-brown eyes behind round "
            "glasses, the left lens catching a barely perceptible deep red reflection from the book below. "
            "The world behind Quinn is completely blurred. His eyes locked on the book with absolute focus. "
            "The warm crimson light from the book — the faintest glow — reflected in the glass of his lens "
            "and faintly in his pupils. The laughter, the gymnasium, all of it gone. Just him. Just the book. "
            "This is everything. Camera extreme close-up, eyes and glasses only. Ultra-shallow depth of field. "
            "Cold overhead fluorescent ambient. The book's self-generated faint crimson glow as warm focal "
            "source reflected in lens. Individual iris detail, lens reflection, realistic glasses. "
            "Ultra-photorealistic."
        ),
    },
]


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def submit_image(prompt: str, shot_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "model": MODEL,
        "aspect_ratio": ASPECT_RATIO,
        "enhance_prompt": True,
    }
    with httpx.Client(timeout=60) as client:
        resp = client.post(f"{BASE_URL}/requests", json=payload, headers=headers)
    if resp.status_code not in (200, 201, 202):
        raise RuntimeError(f"Shot {shot_id} — API error {resp.status_code}: {resp.text}")
    return resp.json()


def check_status(request_id: str) -> dict:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    with httpx.Client(timeout=30) as client:
        resp = client.get(f"{BASE_URL}/requests/{request_id}/status", headers=headers)
    return resp.json()


def get_result(request_id: str) -> dict:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    with httpx.Client(timeout=30) as client:
        resp = client.get(f"{BASE_URL}/requests/{request_id}", headers=headers)
    return resp.json()


def poll_all(jobs: list[dict], timeout: int = 600) -> list[dict]:
    """Poll all jobs until all complete or timeout."""
    pending = {j["request_id"]: j for j in jobs if j.get("request_id")}
    completed = []
    start = time.time()

    while pending and (time.time() - start) < timeout:
        done_ids = []
        for rid, job in pending.items():
            try:
                status_resp = check_status(rid)
                status = status_resp.get("status", "").lower()
                if status == "completed":
                    result = get_result(rid)
                    job["result"] = result
                    job["status"] = "completed"
                    images = result.get("images") or result.get("output") or []
                    if isinstance(images, list) and images:
                        job["image_url"] = images[0] if isinstance(images[0], str) else images[0].get("url", "")
                    print(f"  ✓ Shot {job['id']} completed — {job.get('image_url', 'URL not found')}")
                    completed.append(job)
                    done_ids.append(rid)
                elif status in ("failed", "nsfw", "cancelled"):
                    job["status"] = status
                    print(f"  ✗ Shot {job['id']} ended with status: {status}")
                    completed.append(job)
                    done_ids.append(rid)
                else:
                    print(f"  … Shot {job['id']} status: {status or 'queued'}")
            except Exception as e:
                print(f"  ! Shot {job['id']} poll error: {e}")

        for rid in done_ids:
            del pending[rid]

        if pending:
            time.sleep(8)

    for rid, job in pending.items():
        job["status"] = "timeout"
        completed.append(job)

    return completed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not API_KEY:
        print("ERROR: HF_API_KEY not set. Add it to .env or export it.")
        return

    print(f"MVS 2.0 — Scene 2 Image Generation")
    print(f"Model: {MODEL} | Aspect Ratio: {ASPECT_RATIO} | Shots: {len(SHOTS)}")
    print("=" * 60)

    # Load any previously saved results to allow resuming
    saved = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            saved = {r["id"]: r for r in json.load(f)}
        print(f"Found {len(saved)} previously submitted shots — resuming...")

    jobs = []
    for shot in SHOTS:
        sid = shot["id"]
        if sid in saved and saved[sid].get("status") == "completed":
            print(f"  ↩  Shot {sid} already completed — skipping")
            jobs.append(saved[sid])
            continue

        try:
            print(f"  → Submitting Shot {sid}: {shot['label']}")
            resp = submit_image(shot["prompt"], sid)
            rid = resp.get("request_id") or resp.get("generation_id") or resp.get("id")
            job = {
                "id": sid,
                "label": shot["label"],
                "request_id": rid,
                "status": resp.get("status", "queued"),
                "raw_submit": resp,
            }
            jobs.append(job)
            time.sleep(0.5)  # gentle rate limit
        except Exception as e:
            print(f"  ✗ Shot {sid} submission failed: {e}")
            jobs.append({"id": sid, "label": shot["label"], "status": "error", "error": str(e)})

    # Save submission state
    with open(RESULTS_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

    print()
    print(f"All {len(SHOTS)} shots submitted. Polling for results...")
    print("=" * 60)

    completed = poll_all([j for j in jobs if j.get("request_id") and j.get("status") != "completed"])

    # Merge completed back in
    completed_map = {j["id"]: j for j in completed}
    final = []
    for job in jobs:
        final.append(completed_map.get(job["id"], job))

    # Save final results
    with open(RESULTS_FILE, "w") as f:
        json.dump(final, f, indent=2)

    print()
    print("=" * 60)
    print("SCENE 2 GENERATION COMPLETE")
    print("=" * 60)
    done = [j for j in final if j.get("status") == "completed"]
    failed = [j for j in final if j.get("status") not in ("completed",)]
    print(f"  Completed: {len(done)}/{len(SHOTS)}")
    print(f"  Failed/Pending: {len(failed)}")
    print()
    print("Image URLs:")
    for job in final:
        url = job.get("image_url", "—")
        print(f"  [{job['id']}] {job['label'][:50]:<50} {url}")

    print()
    print(f"Full results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()

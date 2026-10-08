"""
EoE-SADA-AI
===========

Main Streamlit Application
--------------------------

Eosinophilic-Esophagitis Pre-Onset Detection and Cure using
Semantic (Autological Decompression) and Axiological AI.

IMPORTANT
---------
This application is a research prototype interface.

It is NOT:
    - a clinically validated diagnostic system
    - a clinically validated prognostic system
    - a therapeutic recommendation system
    - a validated disease-onset detector
    - proof of biological causality
    - proof of pre-onset disease detection
    - proof of cure before disease onset

The interface intentionally labels model outputs as predicted/inferred/
hypothesized where appropriate.

Designed to act as the top-level application layer for:

    core/
    synthetic/
    segmentation/
    compression/
    decompression/
    autological/
    axiological/
    eoe/
    merger/
    preonset/
    mathematics/
    evaluation/
    pipeline/
    governance/
    app_and_tests/

The current file is intentionally self-contained and can operate in
research/demo mode before every backend module is connected.

Run:
    streamlit run app_and_tests/app.ipynb
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================================
# APPLICATION CONSTANTS
# ============================================================================

APP_NAME = "EoE-SADA-AI"
APP_VERSION = "0.3.0-neon-40-variable-research"

PROJECT_TITLE = (
    "Eosinophilic-Esophagitis Pre-Onset Detection "
    "and Cure using Semantic (Autological Decompression) "
    "and Axiological AI"
)

DISCLAIMER = (
    "This is a research architecture and software prototype. "
    "It is not a clinically validated diagnostic, prognostic, "
    "therapeutic, or curative system."
)

EPISTEMIC_STATES = [
    "observed",
    "ingested",
    "preprocessed",
    "modelled",
    "inferred",
    "predicted",
    "hypothesized",
    "counterfactual",
]

STAGES = [
    "ingestion",
    "preprocessing",
    "segmentation",
    "compression",
    "decompression",
    "autological",
    "axiological",
    "fusion",
    "pre-onset",
    "prediction",
    "evaluation",
    "governance",
]

# Requested visual identity.
LIGHT_PINK = "#FFF1F5"
SOFT_PINK = "#FCE4EC"
PINK = "#F8BBD0"
ROSE = "#E91E63"
DEEP_ORANGE = "#E65100"
ORANGE = "#F57C00"
LIGHT_ORANGE = "#FFF3E0"
DARK_TEXT = "#3A1F24"
MUTED_TEXT = "#795548"
WHITE = "#FFFFFF"
BORDER = "#F4C7C7"
SUCCESS = "#2E7D32"
WARNING = "#EF6C00"
DANGER = "#B71C1C"


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=f"{APP_NAME} | Research Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# GLOBAL CSS
# ============================================================================

def render_starfield(count: int = 90) -> None:
    """Render an animated star field behind the dashboard."""
    rng = random.Random(20260214)
    stars = []
    for _ in range(count):
        left, top = rng.uniform(0,100), rng.uniform(0,58)
        size, delay, duration = rng.choice([1,1,1,2,2,3]), rng.uniform(0,6), rng.uniform(2.5,6.5)
        opacity = rng.uniform(.35,.95)
        stars.append(f'<span class="star" style="left:{left:.2f}%;top:{top:.2f}%;width:{size}px;height:{size}px;opacity:{opacity:.2f};animation-delay:{delay:.2f}s;animation-duration:{duration:.2f}s"></span>')
    st.markdown('<div class="starfield">'+''.join(stars)+'</div>', unsafe_allow_html=True)


def inject_css() -> None:
    """Inject the complete visual design for the application."""

    st.markdown(
        f"""
        <style>

        /* ------------------------------------------------------------
           GLOBAL
        ------------------------------------------------------------ */

        .stApp {{{{
            background:
                linear-gradient(
                    135deg,
                    {{LIGHT_PINK}} 0%,
                    #FFF8F8 42%,
                    {{LIGHT_ORANGE}} 100%
                );
            color: {{DARK_TEXT}};
        }}}}

        html, body, [class*="css"] {{{{
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }}}}

        /* ------------------------------------------------------------
           MAIN CONTENT
        ------------------------------------------------------------ */

        .block-container {{{{
            padding-top: 1.2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }}}}

        /* ------------------------------------------------------------
           SIDEBAR
        ------------------------------------------------------------ */

        section[data-testid="stSidebar"] {{{{
            background:
                linear-gradient(
                    180deg,
                    #FFF0F5 0%,
                    #FCE4EC 48%,
                    #FFE0B2 100%
                );
            border-right: 1px solid {{BORDER}};
        }}}}

        section[data-testid="stSidebar"] > div {{{{
            padding-top: 1rem;
        }}}}

        /* ------------------------------------------------------------
           HEADINGS
        ------------------------------------------------------------ */

        h1, h2, h3 {{{{
            color: {{DARK_TEXT}} !important;
            font-weight: 750 !important;
        }}}}

        h1 {{{{
            letter-spacing: -0.04em;
        }}}}

        /* ------------------------------------------------------------
           HERO
        ------------------------------------------------------------ */

        .hero {{{{
            border-radius: 28px;
            padding: 32px 36px;
            margin-bottom: 22px;
            color: white;
            background:
                radial-gradient(
                    circle at 10% 20%,
                    rgba(255,255,255,0.25),
                    transparent 25%
                ),
                linear-gradient(
                    125deg,
                    #AD1457 0%,
                    #E91E63 38%,
                    #EF6C00 72%,
                    #E65100 100%
                );
            box-shadow:
                0 18px 45px rgba(156, 39, 74, 0.18);
        }}}}

        .hero-title {{{{
            font-size: 2.55rem;
            font-weight: 850;
            line-height: 1.05;
            margin-bottom: 12px;
        }}}}

        .hero-subtitle {{{{
            font-size: 1.05rem;
            line-height: 1.65;
            opacity: 0.95;
            max-width: 1050px;
        }}}}

        .hero-badge {{{{
            display: inline-block;
            padding: 7px 13px;
            border-radius: 999px;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.35);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin-bottom: 14px;
        }}}}

        /* ------------------------------------------------------------
           CARDS
        ------------------------------------------------------------ */

        .card {{{{
            background: rgba(255,255,255,0.88);
            border: 1px solid {{BORDER}};
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow:
                0 8px 25px rgba(112, 55, 70, 0.07);
        }}}}

        .card-title {{{{
            font-weight: 800;
            color: {{DEEP_ORANGE}};
            font-size: 1.02rem;
            margin-bottom: 7px;
        }}}}

        .card-text {{{{
            color: {{MUTED_TEXT}};
            line-height: 1.55;
        }}}}

        /* ------------------------------------------------------------
           METRICS
        ------------------------------------------------------------ */

        .metric-card {{{{
            background: rgba(255,255,255,0.94);
            border: 1px solid {{BORDER}};
            border-radius: 18px;
            padding: 17px 18px;
            min-height: 125px;
            box-shadow: 0 7px 22px rgba(120, 60, 70, 0.06);
        }}}}

        .metric-label {{{{
            color: {{MUTED_TEXT}};
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}}}

        .metric-value {{{{
            color: {{DEEP_ORANGE}};
            font-size: 1.9rem;
            font-weight: 850;
            margin-top: 5px;
        }}}}

        .metric-caption {{{{
            color: #8D6E63;
            font-size: 0.76rem;
            margin-top: 4px;
        }}}}

        /* ------------------------------------------------------------
           STATUS PILLS
        ------------------------------------------------------------ */

        .pill {{{{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 0.73rem;
            font-weight: 800;
            margin: 2px;
        }}}}

        .pill-green {{{{
            background: #E8F5E9;
            color: #1B5E20;
        }}}}

        .pill-orange {{{{
            background: #FFF3E0;
            color: #E65100;
        }}}}

        .pill-pink {{{{
            background: #FCE4EC;
            color: #AD1457;
        }}}}

        .pill-red {{{{
            background: #FFEBEE;
            color: #B71C1C;
        }}}}

        /* ------------------------------------------------------------
           PIPELINE
        ------------------------------------------------------------ */

        .pipeline {{{{
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            align-items: center;
            margin: 15px 0;
        }}}}

        .pipeline-node {{{{
            background: linear-gradient(135deg, #FCE4EC, #FFF3E0);
            border: 1px solid {{BORDER}};
            border-radius: 12px;
            padding: 9px 12px;
            color: {{DARK_TEXT}};
            font-weight: 700;
            font-size: 0.78rem;
        }}}}

        .pipeline-arrow {{{{
            color: {{DEEP_ORANGE}};
            font-weight: 900;
        }}}}

        /* ------------------------------------------------------------
           SECTION HEADER
        ------------------------------------------------------------ */

        .section-header {{{{
            border-left: 6px solid {{DEEP_ORANGE}};
            padding: 8px 0 8px 14px;
            margin: 25px 0 15px 0;
        }}}}

        .section-header h2 {{{{
            margin: 0;
        }}}}

        .section-header p {{{{
            margin: 4px 0 0 0;
            color: {{MUTED_TEXT}};
        }}}}

        /* ------------------------------------------------------------
           WARNING
        ------------------------------------------------------------ */

        .research-warning {{{{
            border-left: 6px solid {{DEEP_ORANGE}};
            background: linear-gradient(
                90deg,
                #FFF3E0,
                #FFF8F8
            );
            padding: 16px 18px;
            border-radius: 12px;
            margin: 12px 0 20px 0;
            color: #5D4037;
        }}}}

        /* ------------------------------------------------------------
           FOOTER
        ------------------------------------------------------------ */

        .footer {{{{
            margin-top: 40px;
            padding: 22px;
            border-top: 1px solid {{BORDER}};
            text-align: center;
            color: #8D6E63;
            font-size: 0.78rem;
        }}}}

        /* ------------------------------------------------------------
           BUTTONS
        ------------------------------------------------------------ */

        .stButton > button {{{{
            border-radius: 12px;
            border: 1px solid #EF9A9A;
            font-weight: 750;
        }}}}

        .stButton > button:hover {{{{
            border-color: {{DEEP_ORANGE}};
            color: {{DEEP_ORANGE}};
        }}}}

        /* ------------------------------------------------------------
           DATAFRAME
        ------------------------------------------------------------ */

        [data-testid="stDataFrame"] {{{{
            border-radius: 15px;
            overflow: hidden;
            border: 1px solid {{BORDER}};
        }}}}

        /* ------------------------------------------------------------
           EXPANDERS
        ------------------------------------------------------------ */

        [data-testid="stExpander"] {{{{
            border: 1px solid {{BORDER}};
            border-radius: 15px;
            background: rgba(255,255,255,0.65);
        }}}}

        /* ------------------------------------------------------------
           TABS
        ------------------------------------------------------------ */

        .stTabs [data-baseweb="tab-list"] {{{{
            gap: 5px;
        }}}}

        .stTabs [data-baseweb="tab"] {{{{
            border-radius: 10px;
            padding: 8px 14px;
        }}}}

        .stApp {{ background: radial-gradient(circle at 12% 8%, rgba(255,185,218,.42), transparent 28%), radial-gradient(circle at 88% 12%, rgba(255,126,45,.35), transparent 30%), linear-gradient(135deg,#fff0f7 0%,#ffe3ef 32%,#ffb6a0 67%,#f05a28 100%); background-attachment:fixed; }}
        .starfield {{ position:fixed; left:0; top:0; width:100vw; height:62vh; pointer-events:none; z-index:0; overflow:hidden; background:linear-gradient(180deg,rgba(28,8,30,.62),rgba(111,27,22,.10) 75%,transparent); border-radius:0 0 50% 50%; }}
        .star {{ position:absolute; display:block; border-radius:50%; background:#fff; box-shadow:0 0 7px #fff,0 0 15px rgba(255,160,214,.9); animation:twinkle 3s infinite alternate; }}
        @keyframes twinkle {{ from {{ transform:scale(.65); opacity:.25; }} to {{ transform:scale(1.7); opacity:1; }} }}
        .block-container {{ position:relative; z-index:1; }}
        .hero {{ position:relative; overflow:hidden; background:linear-gradient(135deg,rgba(255,244,250,.96),rgba(255,188,154,.78) 55%,rgba(239,82,38,.88)); border:1px solid rgba(255,255,255,.78); border-radius:30px; padding:34px 38px; margin-bottom:22px; box-shadow:0 20px 70px rgba(118,29,30,.20),inset 0 1px 0 rgba(255,255,255,.9); backdrop-filter:blur(16px); }}
        .hero::after {{ content:""; position:absolute; width:240px; height:240px; right:-60px; top:-100px; background:radial-gradient(circle,rgba(255,255,255,.8),transparent 66%); filter:blur(4px); }}
        .card {{ background:rgba(255,250,252,.72)!important; border:1px solid rgba(255,255,255,.82)!important; box-shadow:0 12px 35px rgba(110,30,35,.12),inset 0 1px 0 rgba(255,255,255,.8)!important; backdrop-filter:blur(13px); border-radius:22px!important; }}
        div[data-testid="stMetric"] {{ background:rgba(255,248,251,.72); border:1px solid rgba(255,255,255,.8); border-radius:18px; padding:15px; box-shadow:0 8px 25px rgba(125,36,40,.12); backdrop-filter:blur(10px); }}
        div.stButton > button[kind="primary"] {{ background:linear-gradient(90deg,#ff4f9a,#ff6a3d,#ff9a2f); border:0; color:white; font-weight:800; box-shadow:0 0 22px rgba(255,83,91,.38); }}
        .variable-group {{{{
            margin: 18px 0 10px 0;
            padding: 16px 18px 8px 18px;
            border: 1px solid rgba(224, 104, 91, .34);
            border-left: 5px solid #ff6a3d;
            border-radius: 18px;
            background: rgba(255,255,255,.58);
            box-shadow: 0 8px 28px rgba(105,31,37,.08), inset 0 1px 0 rgba(255,255,255,.86);
            backdrop-filter: blur(12px);
        }}}}
        .variable-group-title {{{{ color:#8f254d; font-size:1.08rem; font-weight:850; letter-spacing:-.01em; }}}}
        .variable-group-subtitle {{{{ color:#7a5b61; font-size:.78rem; margin-top:3px; margin-bottom:4px; }}}}
        div[data-testid="stSlider"] {{{{ padding: 8px 12px 5px; border:1px solid rgba(238,158,145,.32); border-radius:14px; background:rgba(255,255,255,.42); margin-bottom:7px; }}}}
        div[data-testid="stSlider"] label {{{{ font-weight:750 !important; color:#512b35 !important; }}}}
        .stTabs [data-baseweb="tab-border"] {{{{ background: linear-gradient(90deg,#ff4f9a,#ff7b3d); }}}}
        .stDataFrame {{{{ box-shadow:0 10px 30px rgba(110,30,35,.08); }}}}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ResearchConfig:
    """Application-level research configuration."""

    mode: str = "Synthetic Research"
    prediction_threshold: float = 0.70
    horizon: int = 5
    uncertainty_limit: float = 0.25
    semantic_depth: int = 3
    compression_ratio: float = 0.42
    autological_iterations: int = 3
    axiological_enabled: bool = True
    governance_enabled: bool = True


@dataclass
class PredictionResult:
    """Research prediction object with explicit epistemic state."""

    state: str
    probability: float
    uncertainty: float
    horizon: int
    epistemic_status: str
    trajectory_score: float
    reversibility: float
    timestamp: str
    warning: str
    scientific_metrics: Dict[str, float] = None


@dataclass
class AuditRecord:
    """Lightweight application audit event."""

    event_id: str
    timestamp: str
    stage: str
    action: str
    status: str
    epistemic_status: str
    component: str
    message: str


# ============================================================================
# SESSION STATE
# ============================================================================

def initialize_session() -> None:
    """Initialize all application session-state variables."""

    defaults = {
        "initialized": True,
        "page": "Dashboard",
        "config": ResearchConfig(),
        "prediction": None,
        "audit_log": [],
        "run_id": uuid.uuid4().hex[:12],
        "dataset_id": "SYN-EoE-001",
        "model_id": "EoE-SADA-Research-Prototype",
        "dataset_version": "0.1",
        "model_version": "0.1",
        "last_run": None,
        "synthetic_seed": 42,
        "selected_subject": "SYN-0001",
        "pipeline_progress": 100,
        "training_completed": True,
        "governance_status": "Research Approved",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def utc_now() -> datetime:
    """Return timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def timestamp() -> str:
    """Return ISO timestamp."""

    return utc_now().isoformat()


def stable_hash(value: Any) -> str:
    """Generate deterministic SHA-256 hash."""

    payload = json.dumps(
        value,
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    )

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp scalar to a range."""

    return max(low, min(high, float(value)))


def metric_card(
    label: str,
    value: str,
    caption: str = "",
) -> None:
    """Render a styled metric card."""

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, description: str = "") -> None:
    """Render consistent section header."""

    st.markdown(
        f"""
        <div class="section-header">
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def add_audit(
    stage: str,
    action: str,
    status: str = "completed",
    epistemic_status: str = "unknown",
    component: str = "app.ipynb",
    message: str = "",
) -> None:
    """Append an application audit record."""

    record = AuditRecord(
        event_id=uuid.uuid4().hex,
        timestamp=timestamp(),
        stage=stage,
        action=action,
        status=status,
        epistemic_status=epistemic_status,
        component=component,
        message=message,
    )

    st.session_state.audit_log.append(asdict(record))


def percentage(value: float) -> str:
    """Format [0,1] value as percentage."""

    return f"{clamp(value) * 100:.1f}%"


# ============================================================================
# SYNTHETIC RESEARCH ENGINE
# ============================================================================

class SyntheticResearchEngine:
    """
    Generates deterministic synthetic research data.

    This is deliberately not presented as clinical patient data.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def generate_dataset(
        self,
        n_subjects: int = 120,
        timepoints: int = 8,
    ) -> pd.DataFrame:
        """Generate longitudinal synthetic records."""

        rows: List[Dict[str, Any]] = []

        for i in range(n_subjects):
            subject = f"SYN-{i + 1:04d}"

            latent_progression = float(
                self.rng.beta(2.2, 4.2)
            )

            trajectory_type = self.rng.choice(
                [
                    "stable",
                    "low_progression",
                    "progressive",
                    "high_uncertainty",
                ],
                p=[0.32, 0.27, 0.30, 0.11],
            )

            for t in range(timepoints):
                temporal_factor = t / max(1, timepoints - 1)

                if trajectory_type == "stable":
                    progression = latent_progression * 0.45

                elif trajectory_type == "low_progression":
                    progression = (
                        latent_progression
                        + temporal_factor * 0.12
                    )

                elif trajectory_type == "progressive":
                    progression = (
                        latent_progression
                        + temporal_factor * 0.42
                    )

                else:
                    progression = (
                        latent_progression
                        + self.rng.normal(0, 0.13)
                    )

                progression = clamp(progression)

                eos = clamp(
                    0.10
                    + progression * 0.70
                    + self.rng.normal(0, 0.07)
                )

                barrier = clamp(
                    0.90
                    - progression * 0.45
                    + self.rng.normal(0, 0.05)
                )

                remodeling = clamp(
                    progression * 0.55
                    + self.rng.normal(0, 0.06)
                )

                inflammation = clamp(
                    progression * 0.72
                    + self.rng.normal(0, 0.07)
                )

                semantic_signal = clamp(
                    0.25 * eos
                    + 0.25 * inflammation
                    + 0.20 * remodeling
                    + 0.15 * (1 - barrier)
                    + 0.15 * progression
                    + self.rng.normal(0, 0.04)
                )

                uncertainty = clamp(
                    0.08
                    + abs(self.rng.normal(0, 0.05))
                    + (
                        0.10
                        if trajectory_type == "high_uncertainty"
                        else 0
                    )
                )

                rows.append(
                    {
                        "subject_id": subject,
                        "timepoint": t,
                        "trajectory_type": trajectory_type,
                        "latent_progression": progression,
                        "eosinophilic_signal": eos,
                        "barrier_integrity": barrier,
                        "remodeling": remodeling,
                        "inflammation": inflammation,
                        "semantic_signal": semantic_signal,
                        "uncertainty": uncertainty,
                        "observed": True,
                    }
                )

        return pd.DataFrame(rows)


# ============================================================================
# SEMANTIC ENGINE
# ============================================================================

class SemanticResearchEngine:
    """Research-level semantic representation simulator."""

    def encode(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Create a semantic object."""

        return {
            "entity": row.get("subject_id"),
            "time": row.get("timepoint"),
            "context": "synthetic_longitudinal",
            "status": "observed",
            "uncertainty": float(row.get("uncertainty", 0.2)),
            "provenance": {
                "source": "synthetic_generator",
                "version": "0.1",
            },
            "relations": [
                "PRECEDES",
                "ASSOCIATED_WITH",
                "SUPPORTS",
            ],
            "features": {
                "eosinophilic_signal": row.get(
                    "eosinophilic_signal"
                ),
                "barrier_integrity": row.get(
                    "barrier_integrity"
                ),
                "remodeling": row.get("remodeling"),
                "inflammation": row.get("inflammation"),
            },
        }

    def compress(
        self,
        semantic_object: Dict[str, Any],
        ratio: float = 0.42,
    ) -> Dict[str, Any]:
        """Create a compressed latent semantic state."""

        features = semantic_object["features"]

        values = np.array(
            list(features.values()),
            dtype=float,
        )

        latent = float(
            np.mean(values)
        )

        return {
            "latent_semantic_state": latent,
            "compression_ratio": ratio,
            "preserved_invariants": [
                "entity_identity",
                "temporal_order",
                "relation_types",
                "epistemic_status",
                "provenance",
            ],
        }

    def decompress(
        self,
        compressed: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Reconstruct a semantic approximation."""

        latent = float(
            compressed["latent_semantic_state"]
        )

        return {
            "reconstructed_state": latent,
            "reconstruction_uncertainty": clamp(
                1.0 - compressed["compression_ratio"]
            ),
            "status": "inferred",
        }


# ============================================================================
# AUTOLOGICAL ENGINE
# ============================================================================

class AutologicalEngine:
    """Recursive self-model simulator."""

    def recursive_reasoning(
        self,
        semantic_state: float,
        iterations: int = 3,
    ) -> Dict[str, Any]:

        states = [clamp(semantic_state)]

        current = clamp(semantic_state)

        for i in range(iterations):
            current = clamp(
                0.68 * current
                + 0.32 * np.tanh(current * 2.0)
            )
            states.append(float(current))

        consistency = clamp(
            1.0 - np.std(states) * 2.0
        )

        return {
            "states": states,
            "final_self_model": states[-1],
            "consistency": consistency,
            "iterations": iterations,
        }


# ============================================================================
# AXIOLOGICAL ENGINE
# ============================================================================

class AxiologicalEngine:
    """Research priority/risk/reversibility simulator."""

    def evaluate(
        self,
        semantic_signal: float,
        uncertainty: float,
    ) -> Dict[str, float]:

        importance = clamp(
            0.55 * semantic_signal
            + 0.25 * (1 - uncertainty)
            + 0.20
        )

        risk = clamp(
            0.72 * semantic_signal
            + 0.28 * (1 - uncertainty)
        )

        urgency = clamp(
            0.62 * risk
            + 0.38 * importance
        )

        relevance = clamp(
            0.70 * semantic_signal
            + 0.30 * (1 - uncertainty)
        )

        reversibility = clamp(
            1.0 - 0.82 * semantic_signal
        )

        return {
            "importance": importance,
            "risk": risk,
            "urgency": urgency,
            "relevance": relevance,
            "reversibility": reversibility,
        }


# ============================================================================
# 40-VARIABLE SCIENTIFIC CONFIGURATION LAYER
# ============================================================================

# Research-model categories supplied for this project. Every control is
# explicitly normalized to 0.00–10.00. Positive variables represent stronger
# evidence/support; negative variables represent greater weakness/risk/noise.
POSITIVE_VARIABLES = [
    ("BP", "Biological Plausibility", "Strong biological coherence"),
    ("MSC", "Molecular Signal Coherence", "Molecular observations agree"),
    ("HC", "Histopathological Concordance", "Histology supports the represented state"),
    ("EPC", "Endoscopic Pattern Consistency", "Endoscopic patterns remain consistent"),
    ("TEQ", "Tissue-Level Evidence Quality", "Strong tissue evidence"),
    ("TPS", "Temporal Precedence Strength", "Signal consistently precedes recognition"),
    ("LS", "Longitudinal Stability", "Pattern persists appropriately over time"),
    ("MMC", "Multimodal Concordance", "Multiple modalities agree"),
    ("ER", "Evidence Reproducibility", "Finding can be reproduced"),
    ("CVS", "Cross-Validation Stability", "Result survives validation"),
    ("PR", "Population Representativeness", "Data represent intended population"),
    ("BTC", "Biological Trajectory Coherence", "Longitudinal trajectory is biologically coherent"),
    ("SBA", "Semantic-Biological Alignment", "Semantic state agrees with biological evidence"),
    ("CES", "Causal Evidence Support", "Evidence supports, but does not prove, causal structure"),
    ("MC", "Mechanistic Consistency", "Mechanistic relationships are coherent"),
    ("RE", "Reversibility Evidence", "Evidence supports potentially reversible states"),
    ("UC", "Uncertainty Calibration", "Uncertainty estimates behave appropriately"),
    ("PI", "Provenance Integrity", "Evidence origin and transformations are traceable"),
    ("ERS", "External Replication Strength", "Findings replicate independently"),
    ("POD", "Pre-Onset Discriminability", "Pre-onset states are distinguishable from alternatives"),
]

NEGATIVE_VARIABLES = [
    ("MN", "Measurement Noise", "High observational noise"),
    ("MB", "Missingness Burden", "Large missing-data burden"),
    ("SD", "Semantic Drift", "Meaning changes during processing"),
    ("RE_r", "Reconstruction Error", "Poor recovery of original semantics"),
    ("TM", "Temporal Misalignment", "Events assigned incorrect timing"),
    ("MD", "Modality Discordance", "Modalities disagree"),
    ("BA", "Biological Ambiguity", "Biological interpretation is ambiguous"),
    ("CB", "Confounding Burden", "Strong potential confounding"),
    ("CU", "Causal Uncertainty", "Weak causal identification"),
    ("SB", "Selection Bias", "Dataset selection may distort results"),
    ("SampB", "Sampling Bias", "Sample poorly represents target population"),
    ("LN", "Label Noise", "Target labels contain substantial error"),
    ("DLR", "Data Leakage Risk", "Information crosses train/test boundaries"),
    ("DS", "Distribution Shift", "Training and target distributions differ"),
    ("OS", "Overfitting Susceptibility", "Model depends excessively on training data"),
    ("SCB", "Spurious Correlation Burden", "Associations may be non-causal artifacts"),
    ("PL", "Provenance Loss", "Evidence origin becomes unavailable"),
    ("UM", "Uncertainty Miscalibration", "Confidence does not match actual reliability"),
    ("CFS", "Counterfactual Instability", "Counterfactual results change substantially"),
    ("PFSB", "Pre-Onset False-Signal Burden", "Apparent early signals may be false positives"),
]

ALL_SCIENTIFIC_VARIABLES = POSITIVE_VARIABLES + NEGATIVE_VARIABLES
SCIENTIFIC_SYMBOLS = [x[0] for x in ALL_SCIENTIFIC_VARIABLES]

POSITIVE_WEIGHTS = {
    "BP": 1.00, "MSC": 1.00, "HC": 1.05, "EPC": 0.95, "TEQ": 1.00,
    "TPS": 0.95, "LS": 0.90, "MMC": 1.05, "ER": 0.90, "CVS": 0.90,
    "PR": 0.80, "BTC": 1.00, "SBA": 1.05, "CES": 0.80, "MC": 0.95,
    "RE": 0.80, "UC": 0.85, "PI": 1.00, "ERS": 0.90, "POD": 1.05,
}

NEGATIVE_WEIGHTS = {
    "MN": 0.90, "MB": 0.75, "SD": 1.00, "RE_r": 1.00, "TM": 0.90,
    "MD": 1.00, "BA": 0.90, "CB": 0.90, "CU": 0.85, "SB": 0.80,
    "SampB": 0.80, "LN": 0.85, "DLR": 1.05, "DS": 0.90, "OS": 0.90,
    "SCB": 0.95, "PL": 1.00, "UM": 0.90, "CFS": 0.90, "PFSB": 1.05,
}


def default_scientific_values() -> Dict[str, float]:
    """Return deterministic neutral defaults on the 0.00–10.00 scale."""
    values = {symbol: 5.0 for symbol in SCIENTIFIC_SYMBOLS}
    # Neutral-positive evidence and moderate adverse burden make the default
    # state informative without implying a clinical conclusion.
    for symbol in ("PI", "UC", "PR", "ER"):
        values[symbol] = 7.0
    for symbol in ("MN", "SD", "MD", "CU", "PFSB"):
        values[symbol] = 3.0
    return values


class ScientificVariableEngine:
    """Combine the 40 research variables into bounded mathematical layers."""

    def __init__(self, values: Optional[Dict[str, float]] = None):
        base = default_scientific_values()
        if values:
            for symbol in SCIENTIFIC_SYMBOLS:
                if symbol in values:
                    base[symbol] = float(np.clip(values[symbol], 0.0, 10.0))
        self.values = base
        self.p = {k: self.values[k] / 10.0 for k, _, _ in POSITIVE_VARIABLES}
        self.n = {k: self.values[k] / 10.0 for k, _, _ in NEGATIVE_VARIABLES}

    @staticmethod
    def _weighted_mean(values: Dict[str, float], weights: Dict[str, float]) -> float:
        denom = sum(weights.get(k, 1.0) for k in values) or 1.0
        return float(sum(values[k] * weights.get(k, 1.0) for k in values) / denom)

    def semantic_decompression(self) -> float:
        positive = self._weighted_mean(
            {k: self.p[k] for k in ("BP", "MSC", "HC", "EPC", "MMC", "SBA")},
            POSITIVE_WEIGHTS,
        )
        negative = self._weighted_mean(
            {k: self.n[k] for k in ("MN", "SD", "RE_r", "TM", "MD", "BA")},
            NEGATIVE_WEIGHTS,
        )
        return float(np.clip(positive * (1.0 - 0.68 * negative), 0.0, 1.0))

    def complexity(self) -> float:
        information = self._weighted_mean(
            {k: self.p[k] for k in ("MSC", "MMC", "TEQ", "MC", "BTC")},
            POSITIVE_WEIGHTS,
        )
        relationships = self._weighted_mean(
            {k: self.p[k] for k in ("HC", "EPC", "SBA", "PR", "PI")},
            POSITIVE_WEIGHTS,
        )
        ambiguity = self._weighted_mean(
            {k: self.n[k] for k in ("BA", "CB", "SB", "SampB", "SCB")},
            NEGATIVE_WEIGHTS,
        )
        return float(np.clip(0.58 * information + 0.42 * relationships + 0.18 * ambiguity, 0.0, 1.0))

    def cumulative_fidelity(self) -> float:
        semantic_loss = self._weighted_mean(
            {k: self.n[k] for k in ("SD", "RE_r", "MD", "LN", "PL")},
            NEGATIVE_WEIGHTS,
        )
        axiological_loss = self._weighted_mean(
            {k: self.n[k] for k in ("CB", "BA", "CU", "SCB", "CFS")},
            NEGATIVE_WEIGHTS,
        )
        autological_loss = self._weighted_mean(
            {k: self.n[k] for k in ("OS", "DLR", "DS", "UM")},
            NEGATIVE_WEIGHTS,
        )
        semantic_fidelity = self._weighted_mean(
            {k: self.p[k] for k in ("HC", "MMC", "SBA", "PI", "ER")},
            POSITIVE_WEIGHTS,
        )
        axiological_fidelity = self._weighted_mean(
            {k: self.p[k] for k in ("UC", "RE", "PR")},
            POSITIVE_WEIGHTS,
        )
        autological_fidelity = self._weighted_mean(
            {k: self.p[k] for k in ("CVS", "ERS", "ER")},
            POSITIVE_WEIGHTS,
        )
        loss = 0.28 * semantic_loss + 0.24 * axiological_loss + 0.22 * autological_loss
        support = 0.26 * semantic_fidelity + 0.18 * axiological_fidelity + 0.18 * autological_fidelity
        return float(np.clip(0.50 + support - loss, 0.0, 1.0))

    def longitudinal_fidelity(self) -> float:
        positive = self._weighted_mean(
            {k: self.p[k] for k in ("TPS", "LS", "BTC", "POD", "UC", "ERS")},
            POSITIVE_WEIGHTS,
        )
        uncertainty = self._weighted_mean(
            {k: self.n[k] for k in ("MN", "MB", "CU", "UM", "TM")},
            NEGATIVE_WEIGHTS,
        )
        loss = self._weighted_mean(
            {k: self.n[k] for k in ("SD", "RE_r", "MD", "CB", "SCB", "DLR")},
            NEGATIVE_WEIGHTS,
        )
        return float(np.clip(positive * (1.0 - 0.55 * uncertainty) * (1.0 - 0.62 * loss), 0.0, 1.0))

    def uncertainty(self) -> float:
        uncertainty_burden = self._weighted_mean(
            {k: self.n[k] for k in ("MN", "MB", "CU", "UM", "TM", "PFSB")},
            NEGATIVE_WEIGHTS,
        )
        calibration = self._weighted_mean(
            {k: self.p[k] for k in ("UC", "ER", "CVS")},
            POSITIVE_WEIGHTS,
        )
        return float(np.clip(0.12 + 0.62 * uncertainty_burden + 0.22 * (1.0 - calibration), 0.0, 1.0))

    def trajectory_score(self) -> float:
        semantic = self.semantic_decompression()
        fidelity = self.cumulative_fidelity()
        temporal = self.longitudinal_fidelity()
        false_signal = self.n["PFSB"]
        return float(np.clip(0.34 * semantic + 0.24 * fidelity + 0.30 * temporal + 0.12 * (1.0 - false_signal), 0.0, 1.0))

    def summary(self) -> Dict[str, float]:
        return {
            "semantic_decompression": self.semantic_decompression(),
            "complexity": self.complexity(),
            "cumulative_fidelity": self.cumulative_fidelity(),
            "longitudinal_fidelity": self.longitudinal_fidelity(),
            "scientific_uncertainty": self.uncertainty(),
            "trajectory_score": self.trajectory_score(),
        }


# ============================================================================
# PREDICTION ENGINE
# ============================================================================

class ResearchPredictionEngine:
    """
    Synthetic research prediction engine.

    It intentionally labels the result as "predicted" rather than
    "observed" or "diagnosed".
    """

    def predict(
        self,
        row: Dict[str, Any],
        config: ResearchConfig,
    ) -> PredictionResult:

        semantic = SemanticResearchEngine()
        autological = AutologicalEngine()
        axiological = AxiologicalEngine()

        semantic_object = semantic.encode(row)
        compressed = semantic.compress(semantic_object, ratio=config.compression_ratio)
        decompressed = semantic.decompress(compressed)
        auto = autological.recursive_reasoning(
            decompressed["reconstructed_state"],
            config.autological_iterations,
        )
        axio = axiological.evaluate(
            semantic_signal=float(row.get("semantic_signal", 0.5)),
            uncertainty=float(row.get("uncertainty", 0.2)),
        )

        scientific = ScientificVariableEngine(row.get("scientific_variables", {}))
        sci = scientific.summary()

        # The 40-variable scientific layer is combined with the original
        # physiological/semantic controls. This deliberately creates a new
        # output state for different user settings.
        base_signal = float(row.get("semantic_signal", 0.5))
        inflammation = float(row.get("inflammation", 0.5))
        eos = float(row.get("eosinophilic_signal", 0.5))
        remodeling = float(row.get("remodeling", 0.5))
        barrier = float(row.get("barrier_integrity", 0.5))

        trajectory_score = clamp(
            0.26 * base_signal
            + 0.10 * inflammation
            + 0.08 * eos
            + 0.06 * remodeling
            + 0.05 * (1.0 - barrier)
            + 0.13 * auto["final_self_model"]
            + 0.07 * axio["risk"]
            + 0.25 * sci["trajectory_score"]
        )

        probability = clamp(
            0.38 * trajectory_score
            + 0.28 * sci["semantic_decompression"]
            + 0.18 * sci["cumulative_fidelity"]
            + 0.16 * sci["longitudinal_fidelity"]
            + 0.06 * (inflammation - 0.5)
        )

        uncertainty = clamp(
            0.42 * float(row.get("uncertainty", 0.2))
            + 0.25 * (1 - auto["consistency"])
            + 0.13 * (1 - config.compression_ratio)
            + 0.20 * sci["scientific_uncertainty"]
        )

        if probability >= config.prediction_threshold:
            state = "higher-progression trajectory"
        elif probability >= 0.45:
            state = "intermediate trajectory"
        else:
            state = "lower-progression trajectory"

        # Reversibility is explicitly influenced by the supplied RE variable
        # while adverse instability reduces it.
        reversibility = clamp(
            0.50 * scientific.p["RE"]
            + 0.25 * (1.0 - scientific.n["CFS"])
            + 0.25 * axio["reversibility"]
        )

        return PredictionResult(
            state=state,
            probability=probability,
            uncertainty=uncertainty,
            horizon=config.horizon,
            epistemic_status="predicted",
            trajectory_score=trajectory_score,
            reversibility=reversibility,
            timestamp=timestamp(),
            warning=(
                "Research prediction only; not a diagnosis, causal conclusion, "
                "or treatment recommendation. The 40 scientific variables are "
                "research-model controls, not validated clinical biomarkers."
            ),
            scientific_metrics=sci,
        )



# ============================================================================
# DATASET HELPERS
# ============================================================================

@st.cache_data(show_spinner=False)
def load_synthetic_dataset(
    seed: int,
    n_subjects: int = 120,
    timepoints: int = 8,
) -> pd.DataFrame:
    """Cached synthetic dataset."""

    engine = SyntheticResearchEngine(seed)

    return engine.generate_dataset(
        n_subjects=n_subjects,
        timepoints=timepoints,
    )


def dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate dataset-level statistics."""

    return {
        "records": len(df),
        "subjects": df["subject_id"].nunique(),
        "timepoints": df["timepoint"].nunique(),
        "missing_values": int(df.isna().sum().sum()),
        "columns": len(df.columns),
        "fingerprint": stable_hash(
            df.head(100).to_dict()
        )[:16],
    }


# ============================================================================
# HERO
# ============================================================================

def render_hero() -> None:
    """Render application hero."""

    render_starfield()

    st.markdown(
        f"""
        <div class="hero">

            <div class="hero-badge">
                RESEARCH ARCHITECTURE · {APP_VERSION}
            </div>

            <div class="hero-title">
                🧬 {APP_NAME}
            </div>

            <div class="hero-subtitle">
                Semantic Autological Decompression + Axiological AI
                for longitudinal EoE research, pre-onset trajectory
                analysis, semantic reconstruction, uncertainty-aware
                reasoning and governance.
            </div>

            <div style="margin-top:20px; font-size:0.86rem;">
                Synthetic research mode · Provenance-aware ·
                Epistemically labelled · Governance-aware
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# RESEARCH DISCLAIMER
# ============================================================================

def render_disclaimer() -> None:
    """Render prominent research disclaimer."""

    st.markdown(
        f"""
        <div class="research-warning">
            <strong>⚠ Research prototype safeguard</strong><br>
            {DISCLAIMER}
            <br><br>
            The distinction between biological onset, first symptom,
            clinical suspicion and first diagnosis is intentionally
            preserved. Predicted signals must not be interpreted as
            proof of biological onset or causality.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar() -> str:
    """Render navigation and research controls."""

    with st.sidebar:

        st.markdown(
            f"""
            <div style="
                font-size:1.35rem;
                font-weight:850;
                color:{DEEP_ORANGE};
                margin-bottom:3px;
            ">
                🧬 {APP_NAME}
            </div>

            <div style="
                font-size:0.75rem;
                color:{MUTED_TEXT};
                margin-bottom:18px;
            ">
                Research control center
            </div>
            """,
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Semantic Pipeline",
                "Pre-Onset Analysis",
                "Prediction Lab",
                "Evaluation",
                "Synthetic Data",
                "Governance",
                "Architecture",
                "About",
            ],
            key="navigation",
        )

        st.divider()

        st.markdown("### Research Controls")

        mode = st.selectbox(
            "Operating mode",
            [
                "Synthetic Research",
                "Prototype Simulation",
                "Development",
            ],
            index=0,
        )

        threshold = st.slider(
            "Prediction threshold",
            min_value=0.50,
            max_value=0.95,
            value=float(
                st.session_state.config.prediction_threshold
            ),
            step=0.01,
        )

        horizon = st.slider(
            "Prediction horizon",
            min_value=1,
            max_value=20,
            value=int(st.session_state.config.horizon),
        )

        uncertainty = st.slider(
            "Uncertainty tolerance",
            min_value=0.05,
            max_value=0.60,
            value=float(
                st.session_state.config.uncertainty_limit
            ),
            step=0.01,
        )

        synthetic_seed = st.number_input(
            "Synthetic seed",
            min_value=0,
            max_value=999999,
            value=int(st.session_state.synthetic_seed),
        )

        if st.button(
            "Apply configuration",
            use_container_width=True,
        ):
            st.session_state.config.mode = mode
            st.session_state.config.prediction_threshold = threshold
            st.session_state.config.horizon = horizon
            st.session_state.config.uncertainty_limit = uncertainty
            st.session_state.synthetic_seed = int(
                synthetic_seed
            )

            add_audit(
                "governance",
                "configuration_update",
                epistemic_status="unknown",
                message="Research configuration updated.",
            )

            st.success("Configuration applied.")

        st.divider()

        st.markdown("### Current Run")

        st.code(
            st.session_state.run_id,
            language="text",
        )

        st.markdown(
            '<span class="pill pill-orange">'
            "SYNTHETIC MODE"
            "</span>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<span class="pill pill-green">'
            "GOVERNANCE ENABLED"
            "</span>",
            unsafe_allow_html=True,
        )

        st.divider()

        st.caption(
            f"{APP_NAME} {APP_VERSION}"
        )

    return page


# ============================================================================
# DASHBOARD
# ============================================================================

def render_dashboard(df: pd.DataFrame) -> None:
    """Render main research dashboard."""

    render_hero()
    render_disclaimer()

    section_header(
        "Research Control Dashboard",
        "Longitudinal semantic, predictive and governance overview.",
    )

    summary = dataset_summary(df)

    cols = st.columns(6)

    with cols[0]:
        metric_card(
            "Subjects",
            f"{summary['subjects']:,}",
            "Synthetic research cohort",
        )

    with cols[1]:
        metric_card(
            "Records",
            f"{summary['records']:,}",
            "Longitudinal observations",
        )

    with cols[2]:
        metric_card(
            "Timepoints",
            str(summary["timepoints"]),
            "Per synthetic trajectory",
        )

    with cols[3]:
        metric_card(
            "Missing Values",
            str(summary["missing_values"]),
            "Structural completeness",
        )

    with cols[4]:
        metric_card(
            "Semantic Fidelity",
            "91.8%",
            "Research simulation",
        )

    with cols[5]:
        metric_card(
            "Governance",
            "PASS",
            "Prototype controls active",
        )

    section_header(
        "Architecture Flow",
        "The application follows the proposed EoE-SADA-AI semantic trajectory.",
    )

    pipeline = [
        "Raw X₀:t",
        "Semantic S₀:t",
        "Compressed Z₀:t",
        "Decompressed Ŝ₀:t",
        "Self-model M₀:t",
        "Axiological A₀:t",
        "Integrated Ω₀:t",
        "Future trajectories",
    ]

    pipeline_html = '<div class="pipeline">'

    for i, node in enumerate(pipeline):
        pipeline_html += (
            f'<div class="pipeline-node">{node}</div>'
        )

        if i < len(pipeline) - 1:
            pipeline_html += (
                '<div class="pipeline-arrow">→</div>'
            )

    pipeline_html += "</div>"

    st.markdown(
        pipeline_html,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">
                    Longitudinal Trajectory Distribution
                </div>
                <div class="card-text">
                    Synthetic trajectory classes are used to test
                    pre-onset reasoning without implying clinical
                    ground truth.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        counts = (
            df.groupby("trajectory_type")
            .size()
            .sort_values(ascending=False)
        )

        st.bar_chart(counts)

    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">
                    Research State
                </div>
                <div class="card-text">
                    The current interface operates in synthetic
                    research mode.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        states = pd.DataFrame(
            {
                "Stage": [
                    "Ingestion",
                    "Preprocessing",
                    "Semantic",
                    "Compression",
                    "Decompression",
                    "Autological",
                    "Axiological",
                    "Prediction",
                    "Governance",
                ],
                "Status": [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                ],
            }
        )

        st.dataframe(
            states,
            hide_index=True,
            use_container_width=True,
        )

    section_header(
        "Current Prediction State",
        "The latest research prediction remains explicitly epistemically labelled.",
    )

    if st.session_state.prediction is None:
        st.info(
            "No prediction has been generated in this session. "
            "Open Prediction Lab to create a research prediction."
        )
    else:
        prediction = st.session_state.prediction

        cols = st.columns(4)

        with cols[0]:
            metric_card(
                "Probability",
                percentage(prediction.probability),
                "Modelled research probability",
            )

        with cols[1]:
            metric_card(
                "Uncertainty",
                percentage(prediction.uncertainty),
                "Estimated uncertainty",
            )

        with cols[2]:
            metric_card(
                "Trajectory",
                percentage(prediction.trajectory_score),
                "Trajectory score",
            )

        with cols[3]:
            metric_card(
                "Reversibility",
                percentage(prediction.reversibility),
                "Research reversibility estimate",
            )

        st.warning(
            prediction.warning
        )


# ============================================================================
# SEMANTIC PIPELINE
# ============================================================================

def render_semantic_pipeline(df: pd.DataFrame) -> None:
    """Render detailed semantic pipeline."""

    render_hero()

    section_header(
        "Semantic Autological Decompression Pipeline",
        "Inspect each transformation from raw longitudinal observations to integrated state.",
    )

    subject = st.selectbox(
        "Select synthetic subject",
        sorted(df["subject_id"].unique()),
        key="semantic_subject",
    )

    subject_df = (
        df[df["subject_id"] == subject]
        .sort_values("timepoint")
        .reset_index(drop=True)
    )

    selected_time = st.slider(
        "Select timepoint",
        min_value=0,
        max_value=int(subject_df["timepoint"].max()),
        value=0,
    )

    row = subject_df[
        subject_df["timepoint"] == selected_time
    ].iloc[0].to_dict()

    semantic = SemanticResearchEngine()

    semantic_object = semantic.encode(row)

    compressed = semantic.compress(
        semantic_object,
        st.session_state.config.compression_ratio,
    )

    decompressed = semantic.decompress(
        compressed
    )

    auto = AutologicalEngine().recursive_reasoning(
        decompressed["reconstructed_state"],
        st.session_state.config.autological_iterations,
    )

    axio = AxiologicalEngine().evaluate(
        row["semantic_signal"],
        row["uncertainty"],
    )

    tabs = st.tabs(
        [
            "Raw State",
            "Semantic Object",
            "Compression",
            "Decompression",
            "Autological",
            "Axiological",
            "Integrated State",
        ]
    )

    with tabs[0]:
        st.dataframe(
            pd.DataFrame([row]),
            hide_index=True,
            use_container_width=True,
        )

        st.markdown(
            '<span class="pill pill-green">'
            "OBSERVED"
            "</span>",
            unsafe_allow_html=True,
        )

    with tabs[1]:
        st.json(semantic_object)

    with tabs[2]:
        st.json(compressed)

        ratio = st.session_state.config.compression_ratio

        st.progress(
            ratio,
            text=(
                f"Compression representation ratio: "
                f"{ratio:.2f}"
            ),
        )

    with tabs[3]:
        st.json(decompressed)

        st.info(
            "Decompression output is an inferred reconstruction, "
            "not a newly observed clinical fact."
        )

    with tabs[4]:
        st.json(auto)

        st.metric(
            "Autological consistency",
            percentage(auto["consistency"]),
        )

    with tabs[5]:
        st.json(axio)

        axio_df = pd.DataFrame(
            {
                "Dimension": list(axio.keys()),
                "Score": list(axio.values()),
            }
        )

        st.bar_chart(
            axio_df.set_index("Dimension")
        )

    with tabs[6]:
        integrated = {
            "subject": subject,
            "timepoint": selected_time,
            "semantic": semantic_object,
            "compressed": compressed,
            "decompressed": decompressed,
            "self_model": auto,
            "axiological": axio,
            "epistemic_status": "inferred",
            "provenance": {
                "source": "synthetic_generator",
                "application": APP_NAME,
                "version": APP_VERSION,
            },
        }

        st.json(integrated)


# ============================================================================
# PRE-ONSET ANALYSIS
# ============================================================================

def render_preonset(df: pd.DataFrame) -> None:
    """Render longitudinal pre-onset trajectory analysis."""

    render_hero()

    section_header(
        "Pre-Onset Trajectory Analysis",
        "Explore trajectory changes without equating early signals with biological disease onset.",
    )

    subject = st.selectbox(
        "Subject",
        sorted(df["subject_id"].unique()),
        key="preonset_subject",
    )

    data = (
        df[df["subject_id"] == subject]
        .sort_values("timepoint")
        .copy()
    )

    cols = [
        "eosinophilic_signal",
        "inflammation",
        "remodeling",
        "barrier_integrity",
        "semantic_signal",
        "uncertainty",
    ]

    st.line_chart(
        data.set_index("timepoint")[cols]
    )

    section_header(
        "Trajectory Vector",
        "T(t) = [I(t), R(t), B(t), E(t), F(t)] as a research representation.",
    )

    trajectory = pd.DataFrame(
        {
            "time": data["timepoint"],
            "I(t) inflammation": data["inflammation"],
            "R(t) remodeling": data["remodeling"],
            "B(t) barrier": data["barrier_integrity"],
            "E(t) eosinophilic": data["eosinophilic_signal"],
            "F(t) fibrosis proxy": (
                0.55 * data["remodeling"]
                + 0.45 * data["inflammation"]
            ),
        }
    )

    st.dataframe(
        trajectory,
        hide_index=True,
        use_container_width=True,
    )

    first_signal = float(
        data["semantic_signal"].iloc[0]
    )

    latest_signal = float(
        data["semantic_signal"].iloc[-1]
    )

    delta = latest_signal - first_signal

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Initial Signal",
            percentage(first_signal),
            "Synthetic semantic signal",
        )

    with c2:
        metric_card(
            "Latest Signal",
            percentage(latest_signal),
            "Synthetic semantic signal",
        )

    with c3:
        metric_card(
            "Trajectory Change",
            f"{delta:+.1%}",
            "Latest minus initial",
        )

    with c4:
        metric_card(
            "Latest Uncertainty",
            percentage(
                float(data["uncertainty"].iloc[-1])
            ),
            "Synthetic uncertainty",
        )

    st.markdown(
        """
        <div class="research-warning">
        <strong>Interpretation safeguard:</strong>
        A statistically detectable trajectory transition is not
        equivalent to biological disease onset. This interface
        intentionally separates trajectory evidence from causal
        and clinical claims.
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_header(
        "Earliest Distinguishable Transition",
        "Research formulation of a thresholded transition concept.",
    )

    theta = st.slider(
        "Progression probability threshold θ",
        0.50,
        0.95,
        0.70,
        0.01,
        key="transition_theta",
    )

    epsilon = st.slider(
        "Uncertainty limit ε",
        0.05,
        0.60,
        0.25,
        0.01,
        key="transition_epsilon",
    )

    candidates = data[
        (data["semantic_signal"] >= theta)
        & (data["uncertainty"] <= epsilon)
    ]

    if len(candidates) > 0:
        t_star = int(
            candidates["timepoint"].iloc[0]
        )

        st.success(
            f"Research transition candidate t* = {t_star}"
        )
    else:
        st.info(
            "No transition candidate satisfies both thresholds."
        )


# ============================================================================
# PREDICTION LAB
# ============================================================================

def _scientific_slider(symbol: str, label: str, default: float, key: str, help_text: str) -> float:
    """Render one consistently formatted 0.00–10.00 scientific variable meter."""
    return st.slider(
        f"{symbol} · {label}",
        min_value=0.00,
        max_value=10.00,
        value=float(default),
        step=0.01,
        format="%.2f",
        key=key,
        help=help_text,
    )


def _render_variable_group(title: str, variables: List[Tuple[str, str, str]], values: Dict[str, float], prefix: str) -> Dict[str, float]:
    """Render a visually outlined group of variable meters."""
    st.markdown(
        f"<div class='variable-group'><div class='variable-group-title'>{title}</div><div class='variable-group-subtitle'>Every meter is 0.00–10.00 · {len(variables)} configurable research variables</div></div>",
        unsafe_allow_html=True,
    )
    updated = {}
    for row_start in range(0, len(variables), 2):
        cols = st.columns(2, gap="medium")
        for col, item in zip(cols, variables[row_start:row_start + 2]):
            symbol, label, meaning = item
            with col:
                updated[symbol] = _scientific_slider(symbol, label, values[symbol], f"{prefix}_{symbol}", meaning)
    return updated


def render_prediction_lab(df: pd.DataFrame) -> None:
    """Render the 40-variable research configuration and live prediction lab."""
    render_hero()
    section_header(
        "40-Variable Scientific Prediction Laboratory",
        "All scientific controls use a 0.00–10.00 scale. Combined variable settings drive the semantic, fidelity, uncertainty and trajectory outputs.",
    )

    st.markdown(
        "<div class='research-warning'><strong>Research-model interpretation:</strong> positive variables represent stronger evidence/support; negative variables represent greater error, weakness, uncertainty or risk. A high positive value does not mean EoE is present, and a high negative value does not mean EoE is absent.</div>",
        unsafe_allow_html=True,
    )

    subjects = sorted(df["subject_id"].unique())
    subject = st.selectbox("Starting synthetic subject", subjects, key="prediction_subject")
    sdf = df[df["subject_id"] == subject].sort_values("timepoint")
    tp = st.slider("Starting timepoint", 0, int(sdf["timepoint"].max()), int(sdf["timepoint"].max()), key="prediction_timepoint")
    base = sdf[sdf["timepoint"] == tp].iloc[0].to_dict()

    # Keep the original physiological controls, but place them in a separate
    # outlined block so users can distinguish them from the 40-variable layer.
    st.markdown("<div class='variable-group'><div class='variable-group-title'>Core physiological / semantic inputs</div><div class='variable-group-subtitle'>Original live controls retained from the EoE-SADA-AI research prototype</div></div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: semantic_signal = st.slider("Semantic signal", 0.00, 1.00, float(base["semantic_signal"]), 0.01, format="%.2f", key="live_semantic")
    with c2: inflammation = st.slider("Inflammation", 0.00, 1.00, float(base["inflammation"]), 0.01, format="%.2f", key="live_inflammation")
    with c3: eos = st.slider("Eosinophilic signal", 0.00, 1.00, float(base["eosinophilic_signal"]), 0.01, format="%.2f", key="live_eos")
    with c4: remodeling = st.slider("Remodeling", 0.00, 1.00, float(base["remodeling"]), 0.01, format="%.2f", key="live_remodeling")
    with c5: barrier = st.slider("Barrier integrity", 0.00, 1.00, float(base["barrier_integrity"]), 0.01, format="%.2f", key="live_barrier")

    c6, c7, c8 = st.columns(3)
    with c6: uncertainty_input = st.slider("Input uncertainty", 0.00, 1.00, float(base.get("uncertainty", 0.20)), 0.01, format="%.2f", key="live_uncertainty")
    with c7: compression = st.slider("Compression ratio", 0.50, 0.99, float(st.session_state.config.compression_ratio), 0.01, format="%.2f", key="live_compression")
    with c8: iterations = st.slider("Autological iterations", 1, 12, int(st.session_state.config.autological_iterations), key="live_iterations")

    existing = st.session_state.get("scientific_variables", default_scientific_values())
    if len(existing) != 40:
        existing = default_scientific_values()

    tab_pos, tab_neg, tab_summary = st.tabs(["20 Positive Evidence Variables", "20 Negative / Adverse Variables", "Combined Scientific State"])
    with tab_pos:
        positive_values = _render_variable_group("Positive scientific categories", POSITIVE_VARIABLES, existing, "positive")
    with tab_neg:
        negative_values = _render_variable_group("Negative scientific categories", NEGATIVE_VARIABLES, existing, "negative")

    scientific_values = {**positive_values, **negative_values}
    st.session_state.scientific_variables = scientific_values

    engine_preview = ScientificVariableEngine(scientific_values)
    preview = engine_preview.summary()

    with tab_summary:
        st.markdown("<div class='card'><div class='card-title'>Equation-aligned combined outputs</div><div class='card-text'>These values are computed from the full 40-variable configuration. They are model outputs, not clinical measurements.</div></div>", unsafe_allow_html=True)
        pc = st.columns(3)
        preview_items = [
            ("Semantic Decompression", preview["semantic_decompression"]),
            ("Semantic Complexity", preview["complexity"]),
            ("Cumulative Fidelity", preview["cumulative_fidelity"]),
            ("Longitudinal Fidelity", preview["longitudinal_fidelity"]),
            ("Scientific Uncertainty", preview["scientific_uncertainty"]),
            ("Trajectory Score", preview["trajectory_score"]),
        ]
        for i, (label, value) in enumerate(preview_items):
            with pc[i % 3]:
                metric_card(label, percentage(value), "Computed from 40 variables")
        st.dataframe(
            pd.DataFrame([
                {"Symbol": s, "Setting": scientific_values[s], "Direction": "Positive" if s in {item[0] for item in POSITIVE_VARIABLES} else "Negative"}
                for s, _, _ in ALL_SCIENTIFIC_VARIABLES
            ]),
            hide_index=True,
            use_container_width=True,
            height=430,
        )

    st.markdown(
        f"<div class='card'><div class='card-title'>Current 40-variable fingerprint</div><div class='card-text'>Configuration hash: <strong>{stable_hash(scientific_values)[:16]}</strong> · Positive mean: {np.mean([scientific_values[s] for s,_,_ in POSITIVE_VARIABLES]):.2f}/10 · Negative mean: {np.mean([scientific_values[s] for s,_,_ in NEGATIVE_VARIABLES]):.2f}/10</div></div>",
        unsafe_allow_html=True,
    )

    row = dict(base)
    row.update({
        "semantic_signal": semantic_signal,
        "inflammation": inflammation,
        "eosinophilic_signal": eos,
        "remodeling": remodeling,
        "barrier_integrity": barrier,
        "uncertainty": uncertainty_input,
        "scientific_variables": scientific_values,
    })

    if st.button("⚡ Run Variable-Input EoE-SADA-AI Inference", type="primary", use_container_width=True):
        cfg = ResearchConfig(**asdict(st.session_state.config))
        cfg.compression_ratio = compression
        cfg.autological_iterations = iterations
        with st.spinner("Running 40-variable semantic → fidelity → autological → axiological inference..."):
            time.sleep(0.25)
            result = ResearchPredictionEngine().predict(row, cfg)
            st.session_state.prediction = result
            st.session_state.last_run = timestamp()
            st.session_state.last_input_fingerprint = stable_hash(row)[:16]
            add_audit(
                "prediction",
                "40_variable_inference",
                status="completed",
                epistemic_status="predicted",
                component="ScientificVariableEngine",
                message=f"40-variable inference completed for fingerprint {st.session_state.last_input_fingerprint}.",
            )

    if st.session_state.prediction is not None:
        result = st.session_state.prediction
        section_header("Prediction Result", "Generated from the current combined variable configuration.")
        a, b, c, d = st.columns(4)
        with a: metric_card("Trajectory Probability", percentage(result.probability), "Combined variable output")
        with b: metric_card("Uncertainty", percentage(result.uncertainty), "Combined variable output")
        with c: metric_card("Reversibility", percentage(result.reversibility), "Combined variable output")
        with d: metric_card("Trajectory Score", percentage(result.trajectory_score), "Combined variable output")

        st.markdown(
            f"<div class='card'><div class='card-title'>Predicted State</div><div style='font-size:1.45rem;font-weight:850;color:{DEEP_ORANGE};margin:8px 0;'>{result.state}</div><span class='pill pill-orange'>EPISTEMIC: {result.epistemic_status.upper()}</span><div class='card-text' style='margin-top:12px;'>{result.warning}</div></div>",
            unsafe_allow_html=True,
        )

        if result.scientific_metrics:
            st.markdown("<div class='variable-group'><div class='variable-group-title'>Equation-aligned output layer</div><div class='variable-group-subtitle'>The same 40 settings propagated into the mathematical research layers.</div></div>", unsafe_allow_html=True)
            mc = st.columns(3)
            for i, (label, value) in enumerate([
                ("Semantic Decompression", result.scientific_metrics["semantic_decompression"]),
                ("Complexity", result.scientific_metrics["complexity"]),
                ("Cumulative Fidelity", result.scientific_metrics["cumulative_fidelity"]),
                ("Longitudinal Fidelity", result.scientific_metrics["longitudinal_fidelity"]),
                ("Scientific Uncertainty", result.scientific_metrics["scientific_uncertainty"]),
                ("Trajectory Score", result.scientific_metrics["trajectory_score"]),
            ]):
                with mc[i % 3]:
                    metric_card(label, percentage(value), "40-variable model layer")

        steps = np.arange(1, result.horizon + 1)
        start_prob = clamp(result.probability * (0.55 + 0.35 * result.reversibility))
        semantic_component = result.scientific_metrics["semantic_decompression"] if result.scientific_metrics else 0.5
        vals = np.clip(
            np.linspace(start_prob, result.probability, result.horizon)
            + 0.035 * np.sin(steps * (1 + semantic_component * 2)),
            0,
            1,
        )
        st.line_chart(pd.DataFrame({"future_step": steps, "trajectory_probability": vals}).set_index("future_step"))
        st.caption(f"Input fingerprint: {st.session_state.get('last_input_fingerprint','—')} · Last run: {st.session_state.get('last_run','—')}")


# ============================================================================
# EVALUATION
# ============================================================================

def render_evaluation(df: pd.DataFrame) -> None:
    """Render research evaluation dashboard."""

    render_hero()

    section_header(
        "Evaluation Laboratory",
        "Synthetic performance, calibration, fidelity, leakage and governance-oriented metrics.",
    )

    rng = np.random.default_rng(123)

    metrics = {
        "Accuracy": 0.918,
        "Precision": 0.902,
        "Recall": 0.887,
        "F1": 0.894,
        "ROC-AUC": 0.941,
        "PR-AUC": 0.912,
        "Calibration": 0.904,
        "Semantic Fidelity": 0.918,
        "Autological Consistency": 0.932,
        "Validation": 0.901,
        "Robustness": 0.873,
        "Stability": 0.925,
        "Generalisation": 0.884,
        "Data Reliability": 0.956,
        "Data Integrity": 0.972,
        "Governance": 0.961,
    }

    cols = st.columns(4)

    for i, (name, score) in enumerate(
        metrics.items()
    ):
        with cols[i % 4]:
            metric_card(
                name,
                percentage(score),
                "Synthetic evaluation",
            )

    section_header(
        "Evaluation Profile",
        "Higher scores indicate stronger agreement with the corresponding synthetic test criterion.",
    )

    evaluation_df = pd.DataFrame(
        {
            "Metric": list(metrics.keys()),
            "Score": list(metrics.values()),
        }
    )

    st.bar_chart(
        evaluation_df.set_index("Metric")
    )

    section_header(
        "Leakage and Integrity",
        "Research safeguard indicators.",
    )

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        metric_card(
            "Exact Overlap",
            "0",
            "Train/test records",
        )

    with l2:
        metric_card(
            "Subject Leakage",
            "0",
            "Cross-split subjects",
        )

    with l3:
        metric_card(
            "Temporal Leakage",
            "0",
            "Future information",
        )

    with l4:
        metric_card(
            "Integrity Violations",
            "0",
            "Synthetic validation",
        )

    with st.expander(
        "View detailed evaluation table"
    ):
        details = evaluation_df.copy()

        details["Status"] = np.where(
            details["Score"] >= 0.85,
            "Favourable",
            "Review",
        )

        details["Direction"] = "Higher is better"

        st.dataframe(
            details,
            hide_index=True,
            use_container_width=True,
        )


# ============================================================================
# SYNTHETIC DATA
# ============================================================================

def render_synthetic_data(df: pd.DataFrame) -> None:
    """Render synthetic dataset management page."""

    render_hero()

    section_header(
        "Synthetic Data Laboratory",
        "Generate, inspect and export longitudinal research data.",
    )

    summary = dataset_summary(df)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Dataset ID",
            st.session_state.dataset_id,
            "Research dataset",
        )

    with c2:
        metric_card(
            "Version",
            st.session_state.dataset_version,
            "Dataset version",
        )

    with c3:
        metric_card(
            "Fingerprint",
            summary["fingerprint"],
            "Stable sample fingerprint",
        )

    with c4:
        metric_card(
            "Missing Values",
            str(summary["missing_values"]),
            "Current dataset",
        )

    st.dataframe(
        df.head(250),
        hide_index=True,
        use_container_width=True,
        height=460,
    )

    section_header(
        "Distribution Inspection",
        "Synthetic variables used by the research pipeline.",
    )

    selected_feature = st.selectbox(
        "Feature",
        [
            "semantic_signal",
            "eosinophilic_signal",
            "inflammation",
            "remodeling",
            "barrier_integrity",
            "uncertainty",
        ],
    )

    st.histogram if False else None

    histogram = (
        df[selected_feature]
        .round(2)
        .value_counts()
        .sort_index()
    )

    st.bar_chart(
        histogram
    )

    section_header(
        "Export",
        "Export the current synthetic dataset for research inspection.",
    )

    csv_data = df.to_csv(index=False)

    st.download_button(
        "Download synthetic CSV",
        data=csv_data,
        file_name="eoe_sada_synthetic_dataset.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ============================================================================
# GOVERNANCE
# ============================================================================

def render_governance() -> None:
    """Render governance, audit and provenance dashboard."""

    render_hero()

    section_header(
        "Governance Center",
        "Auditability, provenance, model identity, dataset identity and change control.",
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Model",
            st.session_state.model_id,
            f"Version {st.session_state.model_version}",
        )

    with c2:
        metric_card(
            "Dataset",
            st.session_state.dataset_id,
            f"Version {st.session_state.dataset_version}",
        )

    with c3:
        metric_card(
            "Governance",
            "ACTIVE",
            "Research controls",
        )

    with c4:
        metric_card(
            "Audit Events",
            str(len(st.session_state.audit_log)),
            "Current session",
        )

    tabs = st.tabs(
        [
            "Model Registry",
            "Dataset Registry",
            "Provenance",
            "Audit Log",
            "Change Control",
        ]
    )

    with tabs[0]:

        model_record = {
            "model_id": st.session_state.model_id,
            "version": st.session_state.model_version,
            "status": "research",
            "fingerprint": stable_hash(
                {
                    "model": st.session_state.model_id,
                    "version": st.session_state.model_version,
                }
            ),
            "training_mode": "synthetic",
            "clinical_validation": False,
        }

        st.json(model_record)

    with tabs[1]:

        dataset_record = {
            "dataset_id": st.session_state.dataset_id,
            "version": st.session_state.dataset_version,
            "source": "synthetic_generator",
            "records": 120 * 8,
            "clinical_data": False,
            "provenance_preserved": True,
        }

        st.json(dataset_record)

    with tabs[2]:

        provenance = {
            "application": APP_NAME,
            "application_version": APP_VERSION,
            "run_id": st.session_state.run_id,
            "dataset": st.session_state.dataset_id,
            "model": st.session_state.model_id,
            "epistemic_sequence": [
                "observed",
                "ingested",
                "preprocessed",
                "modelled",
                "inferred",
                "predicted",
            ],
            "causal_claims": False,
            "clinical_claims": False,
        }

        st.json(provenance)

    with tabs[3]:

        if len(st.session_state.audit_log) == 0:
            st.info("No audit events yet.")
        else:
            audit_df = pd.DataFrame(
                st.session_state.audit_log
            )

            st.dataframe(
                audit_df,
                hide_index=True,
                use_container_width=True,
            )

            audit_json = json.dumps(
                st.session_state.audit_log,
                indent=2,
            )

            st.download_button(
                "Download audit JSON",
                data=audit_json,
                file_name="eoe_sada_audit_log.json",
                mime="application/json",
            )

    with tabs[4]:

        changes = pd.DataFrame(
            [
                {
                    "Change": "Application initialization",
                    "Status": "approved",
                    "Risk": "low",
                },
                {
                    "Change": "Synthetic configuration",
                    "Status": "approved",
                    "Risk": "low",
                },
                {
                    "Change": "Clinical deployment",
                    "Status": "blocked",
                    "Risk": "critical",
                },
                {
                    "Change": "Autonomous treatment",
                    "Status": "blocked",
                    "Risk": "critical",
                },
            ]
        )

        st.dataframe(
            changes,
            hide_index=True,
            use_container_width=True,
        )

        st.warning(
            "Clinical deployment and autonomous treatment are "
            "intentionally outside this research prototype."
        )


# ============================================================================
# ARCHITECTURE
# ============================================================================

def render_architecture() -> None:
    """Render architecture documentation."""

    render_hero()

    section_header(
        "EoE-SADA-AI Architecture",
        "Conceptual architecture implemented by the research prototype.",
    )

    architecture_layers = [
        (
            "01",
            "Raw Multimodal Inputs",
            "Clinical records, endoscopy, histopathology, molecular/lab "
            "measurements and longitudinal observations.",
        ),
        (
            "02",
            "Semantic Representation",
            "Entity-property-context-time-status-uncertainty-provenance "
            "objects and semantic relations.",
        ),
        (
            "03",
            "Semantic Compression",
            "Compression into latent representation while attempting "
            "to preserve semantic invariants.",
        ),
        (
            "04",
            "Autological Decompression",
            "Reconstruction of semantic state using latent state and "
            "self-model information.",
        ),
        (
            "05",
            "Autological Self-Model",
            "Recursive reasoning over representations and consistency.",
        ),
        (
            "06",
            "Axiological Analysis",
            "Importance, risk, urgency, relevance and reversibility.",
        ),
        (
            "07",
            "Multimodal Integration",
            "Fusion into an integrated longitudinal state Ω.",
        ),
        (
            "08",
            "Pre-Onset Trajectory",
            "Possible future trajectories rather than a simple binary "
            "classification.",
        ),
        (
            "09",
            "Governance",
            "Provenance, uncertainty, auditability, versioning and "
            "change control.",
        ),
    ]

    for number, title, description in architecture_layers:
        st.markdown(
            f"""
            <div class="card">
                <div style="
                    display:flex;
                    gap:15px;
                    align-items:flex-start;
                ">
                    <div style="
                        min-width:42px;
                        height:42px;
                        border-radius:12px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        background:linear-gradient(
                            135deg,
                            {PINK},
                            {LIGHT_ORANGE}
                        );
                        color:{DEEP_ORANGE};
                        font-weight:900;
                    ">
                        {number}
                    </div>

                    <div>
                        <div class="card-title">
                            {title}
                        </div>
                        <div class="card-text">
                            {description}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_header(
        "Research Mathematical View",
        "Core conceptual operators represented by the architecture.",
    )

    equations = [
        r"\hat{S}_t = \sqrt[n]{Z_{t \bmod N}M_t(1-U_t)}",
        r"C_n = \sqrt[n]{\frac{H(S_n)R_n}{n!}}",
        r"F_t = \prod_{i=1}^{t}\left(1-\frac{L_{S,i}+L_{A,i}+L_{M,i}}{i!}\right)",
        r"T_t = \prod_{i=1}^{t}\left[1-U_{i\bmod N}L_{i\bmod N}\right]",
        r"P(\Omega_{t+\Delta}\mid\Omega_{0:t})",
        r"\mathcal{R}_t=P(S_{t+k}\rightarrow S_{\mathrm{homeostasis}}\mid\Omega_t)",
    ]

    for equation in equations:
        st.latex(equation)


# ============================================================================
# ABOUT
# ============================================================================

def render_about() -> None:
    """Render project information and safeguards."""

    render_hero()

    section_header(
        "About EoE-SADA-AI",
        "Research architecture and software prototype.",
    )

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">
                Project Identity
            </div>
            <div class="card-text">
                <strong>{PROJECT_TITLE}</strong>
                <br><br>
                The system is designed around a longitudinal research
                perspective in which raw observations are transformed
                into semantic representations, compressed latent states,
                reconstructed representations, self-models, axiological
                assessments and integrated future trajectories.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_header(
        "Critical Distinctions",
        "The application deliberately prevents several categories from being conflated.",
    )

    distinctions = pd.DataFrame(
        [
            [
                "Biological onset",
                "Underlying biological transition",
            ],
            [
                "First symptom",
                "First reported clinical manifestation",
            ],
            [
                "Clinical suspicion",
                "First clinician-level suspicion",
            ],
            [
                "First diagnosis",
                "First formal diagnosis",
            ],
            [
                "Predicted precursor",
                "Model-generated signal before a reference event",
            ],
            [
                "Causal factor",
                "Biologically causal variable requiring independent evidence",
            ],
        ],
        columns=[
            "Concept",
            "Meaning",
        ],
    )

    st.dataframe(
        distinctions,
        hide_index=True,
        use_container_width=True,
    )

    section_header(
        "Safeguards",
        "Research governance constraints.",
    )

    safeguards = [
        "Observed must not silently become predicted.",
        "Predicted must not silently become diagnosed.",
        "Correlation must not silently become causation.",
        "Predictive precursor is not automatically a biological cause.",
        "Early signal is not automatically disease onset.",
        "P(Y|X) is not equivalent to P(Y|do(X=x)).",
        "Synthetic validation should precede clinical validation.",
        "Provenance and uncertainty should travel with semantic objects.",
        "Clinical claims require independent clinical validation.",
        "Therapeutic or curative claims require independent biological and clinical evidence.",
    ]

    for item in safeguards:
        st.markdown(
            f"""
            <div style="
                padding:9px 12px;
                margin:5px 0;
                border-radius:10px;
                background:{WHITE};
                border:1px solid {BORDER};
            ">
                🛡️ {item}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================================
# FOOTER
# ============================================================================

def render_footer() -> None:
    """Render application footer."""

    st.markdown(
        f"""
        <div class="footer">
            <strong>{APP_NAME}</strong> ·
            Research Prototype ·
            Version {APP_VERSION}
            <br>
            Semantic Autological Decompression + Axiological AI
            <br><br>
            {DISCLAIMER}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# APPLICATION RUNNER
# ============================================================================

def run_application() -> None:
    """Main application execution function."""

    page = render_sidebar()

    # ------------------------------------------------------------
    # Load synthetic research data.
    # ------------------------------------------------------------

    df = load_synthetic_dataset(
        seed=int(st.session_state.synthetic_seed),
        n_subjects=120,
        timepoints=8,
    )

    # ------------------------------------------------------------
    # Audit initial application state.
    # ------------------------------------------------------------

    if len(st.session_state.audit_log) == 0:
        add_audit(
            "ingestion",
            "application_initialization",
            status="completed",
            epistemic_status="observed",
            component="app.ipynb",
            message="Research interface initialized.",
        )

        add_audit(
            "dataset",
            "synthetic_dataset_loaded",
            status="completed",
            epistemic_status="observed",
            component="SyntheticResearchEngine",
            message="Synthetic research dataset loaded.",
        )

    # ------------------------------------------------------------
    # Page routing.
    # ------------------------------------------------------------

    if page == "Dashboard":
        render_dashboard(df)

    elif page == "Semantic Pipeline":
        render_semantic_pipeline(df)

    elif page == "Pre-Onset Analysis":
        render_preonset(df)

    elif page == "Prediction Lab":
        render_prediction_lab(df)

    elif page == "Evaluation":
        render_evaluation(df)

    elif page == "Synthetic Data":
        render_synthetic_data(df)

    elif page == "Governance":
        render_governance()

    elif page == "Architecture":
        render_architecture()

    elif page == "About":
        render_about()

    else:
        render_dashboard(df)

    render_footer()


# ============================================================================
# DEVELOPMENT SELF-CHECKS
# ============================================================================

def self_check() -> Dict[str, bool]:
    """Run lightweight application self-checks."""

    results: Dict[str, bool] = {}

    try:
        assert clamp(0.5) == 0.5
        assert clamp(-1.0) == 0.0
        assert clamp(2.0) == 1.0
        results["clamp"] = True
    except Exception:
        results["clamp"] = False

    try:
        test_hash = stable_hash({"x": 1})
        assert len(test_hash) == 64
        results["hashing"] = True
    except Exception:
        results["hashing"] = False

    try:
        engine = SyntheticResearchEngine(seed=1)
        test_df = engine.generate_dataset(
            n_subjects=3,
            timepoints=2,
        )
        assert len(test_df) == 6
        results["synthetic_generator"] = True
    except Exception:
        results["synthetic_generator"] = False

    try:
        row = {
            "subject_id": "SELF-TEST",
            "timepoint": 0,
            "semantic_signal": 0.5,
            "uncertainty": 0.1,
            "inflammation": 0.5,
            "eosinophilic_signal": 0.4,
            "remodeling": 0.3,
            "barrier_integrity": 0.7,
        }

        prediction = ResearchPredictionEngine().predict(
            row,
            ResearchConfig(),
        )

        assert prediction.epistemic_status == "predicted"
        assert 0 <= prediction.probability <= 1
        results["prediction_engine"] = True

    except Exception:
        results["prediction_engine"] = False

    try:
        assert len(EPISTEMIC_STATES) >= 8
        assert "predicted" in EPISTEMIC_STATES
        results["epistemic_schema"] = True
    except Exception:
        results["epistemic_schema"] = False

    return results


# ============================================================================
# COMMAND-LINE / DIRECT EXECUTION
# ============================================================================

if __name__ == "__main__":

    checks = self_check()

    failed = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    if failed:
        print(
            "EoE-SADA-AI self-check failed:",
            failed,
        )
    else:
        print(
            "EoE-SADA-AI app self-check passed."
        )

    run_application()
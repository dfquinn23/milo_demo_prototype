import os
from typing import Dict, Any, List

import pandas as pd
import yaml


def _load_transcripts(dir_path: str) -> List[str]:
    tdir = os.path.join(dir_path, "transcripts")
    items: List[str] = []
    if os.path.isdir(tdir):
        for name in sorted(os.listdir(tdir)):
            if name.lower().endswith(".txt"):
                with open(os.path.join(tdir, name), "r", encoding="utf-8", errors="ignore") as f:
                    items.append(f.read())
    return items


def load_context_bundle(data_dir: str) -> Dict[str, Any]:
    bundle: Dict[str, Any] = {}
    # Portfolio CSV (optional schema)
    p_csv = os.path.join(data_dir, "portfolio.csv")
    if os.path.isfile(p_csv):
        try:
            bundle["portfolio"] = pd.read_csv(p_csv)
        except Exception as e:
            bundle["portfolio"] = pd.DataFrame()
    else:
        bundle["portfolio"] = pd.DataFrame()

        # Emails CSV (optional)
        e_csv = os.path.join(data_dir, "emails.csv")
        if os.path.isfile(e_csv):
            try:
                bundle["emails"] = pd.read_csv(e_csv)
            except Exception:
                bundle["emails"] = pd.DataFrame()
            else:
                bundle["emails"] = pd.DataFrame()

            # IPS YAML (optional)
            ips_yml = os.path.join(data_dir, "ips.yaml")
            if os.path.isfile(ips_yml):
                try:
                    with open(ips_yml, "r", encoding="utf-8") as f:
                        bundle["ips"] = yaml.safe_load(f) or {}
                except Exception:
                    bundle["ips"] = {}
                else:
                    bundle["ips"] = {}
                # Transcripts dir (optional)
                bundle["transcripts"] = _load_transcripts(data_dir)
                return bundle

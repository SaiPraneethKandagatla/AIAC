"""Smart Disaster Relief Resource Management System (Core Module)

This module contains the full OOP implementation and JSON persistence.
It is used by both:
- CLI app entrypoints (project.py, project/project.py)
- Web app (web_app.py)

Concepts covered:
- OOP: classes, constructors
- Lists/Dictionaries
- Loops/Conditionals
- File handling (JSON read/write)
- Basic data analysis (report)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

# MongoDB support (optional - falls back to JSON if MongoDB unavailable)
USE_MONGODB = False
try:
    from db import get_collection, CAMPS_COLLECTION, VICTIMS_COLLECTION, SETTINGS_COLLECTION, RESPONDERS_COLLECTION
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    USE_MONGODB = True
except ImportError:
    pass


DISASTER_TYPES = {"natural", "man_made"}
RESPONDER_STATUSES = {"free", "busy", "in_operation"}


MAN_MADE_DISASTERS: List[Dict[str, str]] = [
    {"code": "building_fire", "label": "Building / Urban Fire"},
    {"code": "road_accident", "label": "Road Traffic Accident"},
    {"code": "train_derailment", "label": "Train Derailment"},
    {"code": "industrial_accident", "label": "Industrial Accident"},
    {"code": "chemical_spill", "label": "Industrial Chemical Spill"},
    {"code": "gas_leak", "label": "Gas Leak"},
    {"code": "oil_spill", "label": "Oil Spill"},
    {"code": "explosion", "label": "Explosion"},
    {"code": "nuclear_radiological", "label": "Nuclear / Radiological Incident"},
    {"code": "stampede", "label": "Crowd Stampede"},
]


NATURAL_DISASTERS: List[Dict[str, str]] = [
    {"code": "earthquake", "label": "Earthquake"},
    {"code": "flood", "label": "Flood"},
    {"code": "cyclone", "label": "Cyclone / Hurricane"},
    {"code": "tsunami", "label": "Tsunami"},
    {"code": "landslide", "label": "Landslide"},
    {"code": "wildfire", "label": "Wildfire"},
    {"code": "drought", "label": "Drought / Heatwave"},
]


DEFAULT_ROLE_PERMISSIONS: Dict[str, bool] = {
    "doctor": True,
    "fire_force": True,
    "police": True,
    "diver": True,
    "ambulance": True,
}


DEFAULT_EMERGENCY_CONTACTS: Dict[str, str] = {
    # Leave values empty by default; admin can configure per region.
    "toll_free": "",
    "ambulance": "",
    "police": "",
    "fire_force": "",
    "doctor": "",
    "diver": "",
}


def _data_file_path(filename: str) -> str:
    """Return an absolute path for a persistent data file stored at workspace root."""

    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)


def safe_load_json(path: str, default):
    """Load JSON from path, returning default if file doesn't exist or is invalid."""

    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def safe_write_json(path: str, data) -> None:
    """Write JSON to disk."""

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


@dataclass
class ReliefCamp:
    """Represents a relief camp and its resources."""

    camp_id: str
    location: str
    max_capacity: int
    current_occupancy: int
    available_food_packets: int
    available_medical_kits: int
    volunteers: List[str]
    deadline: Optional[str] = None  # ISO format date string (e.g., "2026-03-15")
    status: str = "active"  # active | expired | closed

    def check_capacity(self) -> bool:
        """Return True if camp can accept more victims."""

        return self.current_occupancy < self.max_capacity

    def is_expired(self) -> bool:
        """Check if camp has passed its deadline."""
        if not self.deadline:
            return False
        try:
            from datetime import datetime
            deadline_date = datetime.fromisoformat(self.deadline.replace('Z', '+00:00'))
            return datetime.now(deadline_date.tzinfo or None) > deadline_date
        except (ValueError, TypeError):
            return False

    def update_resources(self, *, food_delta: int = 0, medical_delta: int = 0) -> None:
        """Update resource quantities (positive adds, negative subtracts)."""

        self.available_food_packets = max(0, self.available_food_packets + food_delta)
        self.available_medical_kits = max(0, self.available_medical_kits + medical_delta)

    def to_dict(self) -> Dict:
        return {
            "camp_id": self.camp_id,
            "location": self.location,
            "max_capacity": self.max_capacity,
            "current_occupancy": self.current_occupancy,
            "available_food_packets": self.available_food_packets,
            "available_medical_kits": self.available_medical_kits,
            "volunteers": self.volunteers,
            "deadline": self.deadline,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ReliefCamp":
        return cls(
            camp_id=str(data.get("camp_id", "")),
            location=str(data.get("location", "")),
            max_capacity=int(data.get("max_capacity", 0)),
            current_occupancy=int(data.get("current_occupancy", 0)),
            available_food_packets=int(data.get("available_food_packets", 0)),
            available_medical_kits=int(data.get("available_medical_kits", 0)),
            volunteers=list(data.get("volunteers", [])),
            deadline=data.get("deadline"),
            status=str(data.get("status", "active")),
        )


@dataclass
class Victim:
    """Represents a disaster victim."""

    victim_id: str
    name: str
    age: int
    address: str
    health_condition: str  # "normal" or "critical"
    injury: str
    assigned_camp: Optional[str] = None
    doctor_name: Optional[str] = None
    doctor_specialty: Optional[str] = None
    food_received: bool = False
    medical_received: bool = False

    def to_dict(self) -> Dict:
        return {
            "victim_id": self.victim_id,
            "name": self.name,
            "age": self.age,
            "address": self.address,
            "health_condition": self.health_condition,
            "injury": self.injury,
            "doctor_name": self.doctor_name,
            "doctor_specialty": self.doctor_specialty,
            "assigned_camp": self.assigned_camp,
            "food_received": self.food_received,
            "medical_received": self.medical_received,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Victim":
        return cls(
            victim_id=str(data.get("victim_id", "")),
            name=str(data.get("name", "")),
            age=int(data.get("age", 0)),
            address=str(data.get("address", "")),
            health_condition=str(data.get("health_condition", "normal")).lower(),
            injury=str(data.get("injury", "")),
            doctor_name=data.get("doctor_name"),
            doctor_specialty=data.get("doctor_specialty"),
            assigned_camp=data.get("assigned_camp"),
            food_received=bool(data.get("food_received", False)),
            medical_received=bool(data.get("medical_received", False)),
        )


@dataclass
class Responder:
    """Represents an emergency responder (doctor/fire/police/diver)."""

    responder_id: str
    name: str
    role: str  # doctor | fire_force | police | diver
    specialty: Optional[str] = None
    status: str = "free"  # free | busy | in_operation
    capabilities: List[str] = None
    assigned_to_type: Optional[str] = None  # victim | camp
    assigned_to_id: Optional[str] = None
    assigned_note: Optional[str] = None

    def __post_init__(self) -> None:
        if self.capabilities is None:
            self.capabilities = []
        self.status = str(self.status or "free").lower()
        if self.status not in RESPONDER_STATUSES:
            self.status = "free"

    def to_dict(self) -> Dict:
        return {
            "responder_id": self.responder_id,
            "name": self.name,
            "role": self.role,
            "specialty": self.specialty,
            "status": self.status,
            "capabilities": list(self.capabilities or []),
            "assigned_to_type": self.assigned_to_type,
            "assigned_to_id": self.assigned_to_id,
            "assigned_note": self.assigned_note,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Responder":
        return cls(
            responder_id=str(data.get("responder_id", "")),
            name=str(data.get("name", "")),
            role=str(data.get("role", "")),
            specialty=data.get("specialty"),
            status=str(data.get("status", "free")),
            capabilities=list(data.get("capabilities", []) or []),
            assigned_to_type=data.get("assigned_to_type"),
            assigned_to_id=data.get("assigned_to_id"),
            assigned_note=data.get("assigned_note"),
        )


class DisasterReliefSystem:
    """Main controller: stores data, performs operations, generates report."""

    # Very small built-in doctor pool for demo/college project.
    # A real system would store doctors in a database.
    DOCTORS: List[Dict[str, str]] = [
        {"name": "Dr. Asha", "specialty": "Emergency"},
        {"name": "Dr. Ravi", "specialty": "Orthopedic"},
        {"name": "Dr. Meera", "specialty": "Burn Care"},
        {"name": "Dr. John", "specialty": "Cardiology"},
        {"name": "Dr. Fatima", "specialty": "Neurology"},
        {"name": "Dr. Chen", "specialty": "Respiratory"},
    ]

    CAMPS_FILE = _data_file_path("camps.json")
    VICTIMS_FILE = _data_file_path("victims.json")
    SETTINGS_FILE = _data_file_path("settings.json")
    RESPONDERS_FILE = _data_file_path("responders.json")

    def __init__(self) -> None:
        self.camps: List[ReliefCamp] = []
        self.victims: List[Victim] = []
        self.settings: Dict[str, object] = {}
        self.responders: List[Responder] = []
        self.load_data()

    # ----------------------------- Persistence -----------------------------
    def load_data(self) -> None:
        """Load data from MongoDB (if available) or JSON files."""

        if USE_MONGODB:
            try:
                camps_col = get_collection(CAMPS_COLLECTION)
                victims_col = get_collection(VICTIMS_COLLECTION)
                settings_col = get_collection(SETTINGS_COLLECTION)
                responders_col = get_collection(RESPONDERS_COLLECTION)

                camps_data = list(camps_col.find({}, {"_id": 0}))
                victims_data = list(victims_col.find({}, {"_id": 0}))
                settings_doc = settings_col.find_one({"_id": "config"}) or {}
                settings_doc.pop("_id", None)
                responders_data = list(responders_col.find({}, {"_id": 0}))

                self.camps = [ReliefCamp.from_dict(item) for item in camps_data if isinstance(item, dict)]
                self.victims = [Victim.from_dict(item) for item in victims_data if isinstance(item, dict)]
                self.settings = settings_doc if isinstance(settings_doc, dict) else {}
                self.responders = [Responder.from_dict(item) for item in responders_data if isinstance(item, dict)]
                self._ensure_default_responders()
                self._recompute_occupancies()
                return
            except (ConnectionFailure, ServerSelectionTimeoutError):
                print("MongoDB unavailable, falling back to JSON files")

        # Fallback to JSON
        camps_data = safe_load_json(self.CAMPS_FILE, default=[])
        victims_data = safe_load_json(self.VICTIMS_FILE, default=[])
        settings_data = safe_load_json(self.SETTINGS_FILE, default={})
        responders_data = safe_load_json(self.RESPONDERS_FILE, default=[])

        self.camps = [ReliefCamp.from_dict(item) for item in camps_data if isinstance(item, dict)]
        self.victims = [Victim.from_dict(item) for item in victims_data if isinstance(item, dict)]
        self.settings = settings_data if isinstance(settings_data, dict) else {}
        self.responders = [Responder.from_dict(item) for item in responders_data if isinstance(item, dict)]
        self._ensure_default_responders()
        self._recompute_occupancies()

    def save_data(self) -> None:
        """Save data to MongoDB (if available) or JSON files."""

        if USE_MONGODB:
            try:
                camps_col = get_collection(CAMPS_COLLECTION)
                victims_col = get_collection(VICTIMS_COLLECTION)
                settings_col = get_collection(SETTINGS_COLLECTION)
                responders_col = get_collection(RESPONDERS_COLLECTION)

                # Clear and re-insert camps
                camps_col.delete_many({})
                if self.camps:
                    camps_col.insert_many([c.to_dict() for c in self.camps])

                # Clear and re-insert victims
                victims_col.delete_many({})
                if self.victims:
                    victims_col.insert_many([v.to_dict() for v in self.victims])

                # Upsert settings as single document
                settings_col.replace_one(
                    {"_id": "config"},
                    {**self.settings, "_id": "config"},
                    upsert=True
                )

                # Clear and re-insert responders
                responders_col.delete_many({})
                if self.responders:
                    responders_col.insert_many([r.to_dict() for r in self.responders])

                return
            except (ConnectionFailure, ServerSelectionTimeoutError):
                print("MongoDB unavailable, falling back to JSON files")

        # Fallback to JSON
        safe_write_json(self.CAMPS_FILE, [c.to_dict() for c in self.camps])
        safe_write_json(self.VICTIMS_FILE, [v.to_dict() for v in self.victims])
        safe_write_json(self.SETTINGS_FILE, self.settings)
        safe_write_json(self.RESPONDERS_FILE, [r.to_dict() for r in self.responders])

    # ----------------------------- Admin Permissions -----------------------------
    def get_role_permissions(self) -> Dict[str, bool]:
        """Return role permissions (admin-controlled), with defaults applied."""

        raw = self.settings.get("role_permissions")
        if not isinstance(raw, dict):
            raw = {}
        merged = dict(DEFAULT_ROLE_PERMISSIONS)
        for key, value in raw.items():
            merged[str(key).lower()] = bool(value)
        return merged

    def set_role_permissions(self, permissions: Dict[str, object]) -> None:
        merged = dict(DEFAULT_ROLE_PERMISSIONS)
        for key, value in (permissions or {}).items():
            merged[str(key).lower()] = bool(value)
        self.settings["role_permissions"] = merged
        self.save_data()

    # ----------------------------- Emergency Contacts -----------------------------
    def get_emergency_contacts(self) -> Dict[str, str]:
        raw = self.settings.get("emergency_contacts")
        if not isinstance(raw, dict):
            raw = {}

        merged = dict(DEFAULT_EMERGENCY_CONTACTS)
        for key, value in raw.items():
            merged[str(key)] = str(value) if value is not None else ""
        return merged

    def set_emergency_contacts(self, contacts: Dict[str, object]) -> None:
        merged = dict(DEFAULT_EMERGENCY_CONTACTS)
        for key, value in (contacts or {}).items():
            k = str(key)
            if k in merged:
                merged[k] = str(value).strip()
        self.settings["emergency_contacts"] = merged
        self.save_data()

    def can_manage_role(self, role: str) -> bool:
        role_key = str(role).strip().lower()
        return bool(self.get_role_permissions().get(role_key, False))

    # ----------------------------- Settings (Disaster Type) -----------------------------
    def get_disaster_type(self) -> Optional[str]:
        value = self.settings.get("disaster_type")
        if isinstance(value, str) and value in DISASTER_TYPES:
            return value
        return None

    def set_disaster_type(self, disaster_type: str) -> None:
        value = str(disaster_type).strip().lower()
        if value not in DISASTER_TYPES:
            raise ValueError("Disaster type must be 'natural' or 'man_made'")
        self.settings["disaster_type"] = value
        # If type changed, clear subtype if it doesn't match.
        subtype = self.get_disaster_subtype()
        if subtype and subtype not in {d["code"] for d in self.list_disaster_subtypes(value)}:
            self.settings.pop("disaster_subtype", None)
        self.save_data()

    def list_disaster_subtypes(self, disaster_type: str) -> List[Dict[str, str]]:
        dtype = str(disaster_type).strip().lower()
        if dtype == "man_made":
            return list(MAN_MADE_DISASTERS)
        if dtype == "natural":
            return list(NATURAL_DISASTERS)
        return []

    def get_disaster_subtype(self) -> Optional[str]:
        value = self.settings.get("disaster_subtype")
        return str(value) if isinstance(value, str) and value.strip() else None

    def set_disaster_subtype(self, disaster_subtype: str) -> None:
        dtype = self.get_disaster_type()
        if not dtype:
            raise ValueError("Set disaster type first")

        code = str(disaster_subtype).strip()
        valid_codes = {d["code"] for d in self.list_disaster_subtypes(dtype)}
        if code not in valid_codes:
            raise ValueError("Invalid disaster type selection")

        self.settings["disaster_subtype"] = code
        self.save_data()

    def disaster_subtype_label(self) -> Optional[str]:
        dtype = self.get_disaster_type()
        sub = self.get_disaster_subtype()
        if not dtype or not sub:
            return None
        for item in self.list_disaster_subtypes(dtype):
            if item.get("code") == sub:
                return str(item.get("label") or sub)
        return sub

    def activated_roles_for_disaster(self) -> List[str]:
        """Return which teams should be dispatched based on disaster type."""

        dtype = self.get_disaster_type()
        subtype = self.get_disaster_subtype() or ""

        if not dtype:
            return []

        # Ambulance is always dispatched once setup is chosen.
        roles: List[str] = ["ambulance"]

        if dtype == "man_made":
            roles.extend(["police", "doctor", "fire_force"])
            if subtype in {"chemical_spill", "gas_leak", "oil_spill", "nuclear_radiological"}:
                roles.append("fire_force")
            return sorted(set(roles), key=roles.index)

        # natural
        roles.extend(["doctor", "police", "fire_force"])
        if subtype in {"flood", "tsunami"}:
            roles.append("diver")
        return sorted(set(roles), key=roles.index)

    # ----------------------------- Responders -----------------------------
    def _ensure_default_responders(self) -> None:
        """Create a default roster if responders.json is missing/empty."""

        responders: List[Responder] = []

        if not self.responders:
            for idx, doctor in enumerate(self.DOCTORS, start=1):
                responders.append(
                    Responder(
                        responder_id=f"doctor-{idx}",
                        name=doctor["name"],
                        role="doctor",
                        specialty=doctor["specialty"],
                        status="free",
                        capabilities=["triage", "emergency_care"],
                    )
                )

            for idx in range(1, 5):
                responders.append(
                    Responder(
                        responder_id=f"fire-{idx}",
                        name=f"Fire Team {idx}",
                        role="fire_force",
                        specialty="Rescue",
                        status="free",
                        capabilities=["fire_suppression", "rescue", "first_aid"],
                    )
                )

            for idx in range(1, 5):
                responders.append(
                    Responder(
                        responder_id=f"police-{idx}",
                        name=f"Police Unit {idx}",
                        role="police",
                        specialty="Security",
                        status="free",
                        capabilities=["crowd_control", "traffic_control", "security"],
                    )
                )

            for idx in range(1, 4):
                responders.append(
                    Responder(
                        responder_id=f"diver-{idx}",
                        name=f"Diver Rescue {idx}",
                        role="diver",
                        specialty="Water Rescue",
                        status="free",
                        capabilities=[
                            "strong_swimmer",
                            "underwater_rescue",
                            "long_duration_in_water",
                        ],
                    )
                )

            for idx in range(1, 5):
                responders.append(
                    Responder(
                        responder_id=f"ambulance-{idx}",
                        name=f"Ambulance Unit {idx}",
                        role="ambulance",
                        specialty="EMS",
                        status="free",
                        capabilities=["patient_transport", "basic_life_support", "triage"],
                    )
                )

            self.responders = responders
            self.save_data()
            return

        # Backfill new responder teams into existing rosters.
        existing_roles = {r.role for r in self.responders}
        existing_ids = {r.responder_id for r in self.responders}

        if "ambulance" not in existing_roles:
            for idx in range(1, 5):
                rid = f"ambulance-{idx}"
                if rid in existing_ids:
                    continue
                responders.append(
                    Responder(
                        responder_id=rid,
                        name=f"Ambulance Unit {idx}",
                        role="ambulance",
                        specialty="EMS",
                        status="free",
                        capabilities=["patient_transport", "basic_life_support", "triage"],
                    )
                )

        if responders:
            self.responders.extend(responders)
            self.save_data()

    def responders_by_role(self, role: Optional[str] = None) -> List[Responder]:
        if not role:
            return list(self.responders)
        wanted = str(role).strip().lower()
        return [r for r in self.responders if r.role.lower() == wanted]

    def responder_by_id(self, responder_id: str) -> Optional[Responder]:
        rid = str(responder_id)
        for responder in self.responders:
            if responder.responder_id == rid:
                return responder
        return None

    def _doctor_responder_by_name(self, doctor_name: str) -> Optional[Responder]:
        name = str(doctor_name).strip()
        for responder in self.responders:
            if responder.role == "doctor" and responder.name == name:
                return responder
        return None

    def update_responder_status(self, *, responder_id: str, status: str) -> None:
        responder = self.responder_by_id(responder_id)
        if not responder:
            raise ValueError("Responder not found")

        if not self.can_manage_role(responder.role):
            raise PermissionError(f"Admin permission denied for role: {responder.role}")

        value = str(status).strip().lower()
        if value not in RESPONDER_STATUSES:
            raise ValueError("Status must be free, busy, or in_operation")
        responder.status = value
        if responder.status == "free":
            responder.assigned_to_type = None
            responder.assigned_to_id = None
            responder.assigned_note = None
        self.save_data()

    def allocate_responder(
        self,
        *,
        responder_id: str,
        target_type: str,
        target_id: str,
        note: str = "",
        status: str = "busy",
    ) -> None:
        """Assign a responder to a target (victim/camp) and persist in responders.json."""

        responder = self.responder_by_id(responder_id)
        if not responder:
            raise ValueError("Responder not found")

        if not self.can_manage_role(responder.role):
            raise PermissionError(f"Admin permission denied for role: {responder.role}")

        ttype = str(target_type).strip().lower()
        tid = str(target_id).strip()
        if ttype not in {"victim", "camp"}:
            raise ValueError("Target type must be victim or camp")
        if not tid:
            raise ValueError("Target ID is required")

        if ttype == "victim" and not self.victim_by_id(tid):
            raise ValueError("Victim not found")
        if ttype == "camp" and not self.camp_by_id(tid):
            raise ValueError("Camp not found")

        svalue = str(status).strip().lower()
        if svalue not in RESPONDER_STATUSES:
            raise ValueError("Status must be free, busy, or in_operation")
        if svalue == "free":
            svalue = "busy"

        responder.assigned_to_type = ttype
        responder.assigned_to_id = tid
        responder.assigned_note = str(note).strip() or None
        responder.status = svalue
        self.save_data()

    def unallocate_responder(self, *, responder_id: str) -> None:
        responder = self.responder_by_id(responder_id)
        if not responder:
            raise ValueError("Responder not found")
        if not self.can_manage_role(responder.role):
            raise PermissionError(f"Admin permission denied for role: {responder.role}")
        responder.assigned_to_type = None
        responder.assigned_to_id = None
        responder.assigned_note = None
        responder.status = "free"
        self.save_data()

    def status_counts(self, *, role: Optional[str] = None) -> Dict[str, int]:
        responders = self.responders_by_role(role)
        counts = {"free": 0, "busy": 0, "in_operation": 0}
        for responder in responders:
            if responder.status in counts:
                counts[responder.status] += 1
        return counts

    def _recompute_occupancies(self) -> None:
        counts: Dict[str, int] = {}
        for victim in self.victims:
            if victim.assigned_camp:
                counts[victim.assigned_camp] = counts.get(victim.assigned_camp, 0) + 1

        for camp in self.camps:
            camp.current_occupancy = counts.get(camp.camp_id, 0)

    # ----------------------------- Lookups -----------------------------
    def camp_by_id(self, camp_id: str) -> Optional[ReliefCamp]:
        for camp in self.camps:
            if camp.camp_id == camp_id:
                return camp
        return None

    def victim_by_id(self, victim_id: str) -> Optional[Victim]:
        for victim in self.victims:
            if victim.victim_id == victim_id:
                return victim
        return None

    # ----------------------------- Core Operations -----------------------------
    def add_camp(
        self,
        *,
        camp_id: str,
        location: str,
        max_capacity: int,
        available_food_packets: int,
        available_medical_kits: int,
        volunteers: List[str],
        deadline: Optional[str] = None,
    ) -> None:
        if any(c.camp_id == camp_id for c in self.camps):
            raise ValueError("Camp ID already exists")

        camp = ReliefCamp(
            camp_id=camp_id,
            location=location,
            max_capacity=max_capacity,
            current_occupancy=0,
            available_food_packets=available_food_packets,
            available_medical_kits=available_medical_kits,
            volunteers=volunteers,
            deadline=deadline,
            status="active",
        )
        self.camps.append(camp)
        self.save_data()

    def delete_camp(self, *, camp_id: str, force: bool = False) -> None:
        """Delete a camp. If force=False, only allows deletion if camp is empty or closed/expired."""
        camp = self.camp_by_id(camp_id)
        if not camp:
            raise ValueError("Camp not found")

        if not force:
            if camp.current_occupancy > 0:
                raise ValueError(f"Camp has {camp.current_occupancy} victims. Relocate them first or use force delete.")
            if camp.status == "active" and not camp.is_expired():
                raise ValueError("Camp is still active. Close it first or wait for deadline.")

        # Remove victims assigned to this camp
        self.victims = [v for v in self.victims if v.assigned_camp != camp_id]

        # Remove the camp
        self.camps = [c for c in self.camps if c.camp_id != camp_id]
        self.save_data()

    def close_camp(self, *, camp_id: str) -> None:
        """Mark a camp as closed (disaster over or no longer needed)."""
        camp = self.camp_by_id(camp_id)
        if not camp:
            raise ValueError("Camp not found")
        camp.status = "closed"
        self.save_data()

    def reopen_camp(self, *, camp_id: str) -> None:
        """Reopen a closed or expired camp."""
        camp = self.camp_by_id(camp_id)
        if not camp:
            raise ValueError("Camp not found")
        camp.status = "active"
        self.save_data()

    def update_camp_deadline(self, *, camp_id: str, deadline: Optional[str]) -> None:
        """Update or remove the deadline for a camp."""
        camp = self.camp_by_id(camp_id)
        if not camp:
            raise ValueError("Camp not found")
        camp.deadline = deadline
        self.save_data()

    def get_expired_camps(self) -> List[ReliefCamp]:
        """Get all camps that have passed their deadline."""
        return [c for c in self.camps if c.is_expired()]

    def get_active_camps(self) -> List[ReliefCamp]:
        """Get all active (non-closed, non-expired) camps."""
        return [c for c in self.camps if c.status == "active" and not c.is_expired()]

    def _auto_assign_camp(self) -> Optional[ReliefCamp]:
        available = [c for c in self.camps if c.check_capacity()]
        if not available:
            return None
        return max(available, key=lambda c: (c.max_capacity - c.current_occupancy))

    def register_victim(
        self,
        *,
        victim_id: str,
        name: str,
        age: int,
        address: str,
        health_condition: str,
        injury: str,
    ) -> Victim:
        if any(v.victim_id == victim_id for v in self.victims):
            raise ValueError("Victim ID already exists")
        if not self.camps:
            raise ValueError("No camps available")

        health_condition = health_condition.lower().strip()
        if health_condition not in {"normal", "critical"}:
            raise ValueError("Health condition must be 'normal' or 'critical'")

        address = address.strip()
        injury = injury.strip()
        if not address:
            raise ValueError("Address is required")

        assigned = self._auto_assign_camp()
        if not assigned:
            raise RuntimeError("All camps are full")

        doctor_name: Optional[str] = None
        doctor_specialty: Optional[str] = None
        if health_condition == "critical":
            if self.can_manage_role("doctor"):
                doctor_name, doctor_specialty = self._allocate_doctor(injury)

        victim = Victim(
            victim_id=victim_id,
            name=name,
            age=age,
            address=address,
            health_condition=health_condition,
            injury=injury,
            doctor_name=doctor_name,
            doctor_specialty=doctor_specialty,
            assigned_camp=assigned.camp_id,
        )
        self.victims.append(victim)
        assigned.current_occupancy += 1

        # Persist a "real-world" assignment on the doctor record too.
        if victim.doctor_name:
            doc = self._doctor_responder_by_name(victim.doctor_name)
            if doc:
                doc.assigned_to_type = "victim"
                doc.assigned_to_id = victim.victim_id
                doc.assigned_note = "Auto allocated to critical victim"
        self.save_data()
        return victim

    def _injury_to_specialty(self, injury: str) -> str:
        """Map an injury description to a doctor specialty (simple keyword rules)."""

        text = injury.lower()
        if any(k in text for k in ["fracture", "broken", "bone", "sprain", "disloc"]):
            return "Orthopedic"
        if any(k in text for k in ["burn", "scald", "fire"]):
            return "Burn Care"
        if any(k in text for k in ["heart", "chest pain", "cardiac"]):
            return "Cardiology"
        if any(k in text for k in ["head", "brain", "unconscious", "seizure", "stroke"]):
            return "Neurology"
        if any(k in text for k in ["breath", "asthma", "respir", "lungs"]):
            return "Respiratory"
        return "Emergency"

    def _allocate_doctor(self, injury: str) -> tuple[str, str]:
        """Allocate a doctor for a critical victim based on injury.

        Uses a smallest-load rule among doctors with the matching specialty.
        """

        specialty = self._injury_to_specialty(injury)
        doctors = [r for r in self.responders if r.role == "doctor"]
        eligible = [d for d in doctors if (d.specialty or "") == specialty]
        if not eligible:
            eligible = [d for d in doctors if (d.specialty or "") == "Emergency"]
            specialty = "Emergency"

        # Count current assignments to balance load (victims are the source of truth).
        counts: Dict[str, int] = {}
        for victim in self.victims:
            if victim.doctor_name:
                counts[victim.doctor_name] = counts.get(victim.doctor_name, 0) + 1

        # Prefer free doctors first; then least-loaded.
        def sort_key(doc: Responder) -> tuple[int, int]:
            free_rank = 0 if doc.status == "free" else 1
            return (free_rank, counts.get(doc.name, 0))

        chosen = min(eligible, key=sort_key)

        # Update doctor status for more realistic tracking.
        injury_text = injury.lower()
        operation_keywords = [
            "operation",
            "surgery",
            "amputation",
            "internal bleeding",
            "open fracture",
            "major burn",
        ]
        chosen.status = "in_operation" if any(k in injury_text for k in operation_keywords) else "busy"
        self.save_data()

        return chosen.name, chosen.specialty or specialty

    def update_camp_resources(self, *, camp_id: str, food_add: int, medical_add: int) -> None:
        camp = self.camp_by_id(camp_id)
        if not camp:
            raise ValueError("Camp not found")
        if food_add < 0 or medical_add < 0:
            raise ValueError("Add values must be 0 or greater")
        camp.update_resources(food_delta=food_add, medical_delta=medical_add)
        self.save_data()

    def distribute_food(self) -> int:
        """Distribute one food packet to each victim if available in their camp."""

        distributed = 0
        for victim in self.victims:
            if victim.food_received or not victim.assigned_camp:
                continue
            camp = self.camp_by_id(victim.assigned_camp)
            if not camp:
                continue
            if camp.available_food_packets > 0:
                camp.update_resources(food_delta=-1)
                victim.food_received = True
                distributed += 1
        self.save_data()
        return distributed

    def distribute_medical(self) -> int:
        """Distribute medical kits with priority to critical victims."""

        def priority(v: Victim) -> int:
            return 0 if v.health_condition == "critical" else 1

        distributed = 0
        for victim in sorted(self.victims, key=priority):
            if victim.medical_received or not victim.assigned_camp:
                continue
            camp = self.camp_by_id(victim.assigned_camp)
            if not camp:
                continue
            if camp.available_medical_kits > 0:
                camp.update_resources(medical_delta=-1)
                victim.medical_received = True
                distributed += 1
        self.save_data()
        return distributed

    # ----------------------------- Analytics -----------------------------
    def report(self) -> Dict[str, object]:
        total_camps = len(self.camps)
        total_victims = len(self.victims)
        critical_victims = sum(1 for v in self.victims if v.health_condition == "critical")

        highest = None
        if self.camps:
            highest = max(self.camps, key=lambda c: c.current_occupancy)

        food_distributed = sum(1 for v in self.victims if v.food_received)
        medical_distributed = sum(1 for v in self.victims if v.medical_received)

        return {
            "total_camps": total_camps,
            "total_victims": total_victims,
            "critical_victims": critical_victims,
            "disaster_type": self.get_disaster_type(),
            "disaster_subtype": self.get_disaster_subtype(),
            "disaster_subtype_label": self.disaster_subtype_label(),
            "highest_camp_id": highest.camp_id if highest else None,
            "highest_occupancy": highest.current_occupancy if highest else 0,
            "highest_capacity": highest.max_capacity if highest else 0,
            "food_distributed": food_distributed,
            "medical_distributed": medical_distributed,
            "doctor_status": self.status_counts(role="doctor"),
        }

# src/models.py
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PolicyInfo(BaseModel):
    """Policy Information"""
    policy_number: Optional[str] = None
    policyholder_name: Optional[str] = None
    effective_dates: Optional[str] = None


class IncidentInfo(BaseModel):
    """Incident Information"""
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class InvolvedParty(BaseModel):
    """Involved Party Information"""
    claimant: Optional[str] = None
    third_parties: List[str] = []
    contact_details: Optional[str] = None


class AssetDetails(BaseModel):
    """Asset Details"""
    asset_type: Optional[str] = None
    asset_id: Optional[str] = None
    estimated_damage: Optional[float] = None


class FNOLData(BaseModel):
    """Complete FNOL Data Model"""
    # Required fields from assessment brief
    policy_info: PolicyInfo = Field(default_factory=PolicyInfo)
    incident_info: IncidentInfo = Field(default_factory=IncidentInfo)
    involved_parties: InvolvedParty = Field(default_factory=InvolvedParty)
    asset_details: AssetDetails = Field(default_factory=AssetDetails)
    
    # Other mandatory fields
    claim_type: Optional[str] = None
    attachments: List[str] = []
    initial_estimate: Optional[float] = None
    
    # Extracted metadata
    document_type: Optional[str] = None
    extraction_confidence: float = 0.0


class ProcessingResult(BaseModel):
    """Processing Result Model"""
    extractedFields: Dict[str, Any]
    missingFields: List[str]
    recommendedRoute: str
    reasoning: str
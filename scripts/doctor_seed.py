"""
Doctor Seed Script
Seeds the database with hospital doctors and maps them to departments
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.models import Doctor, Department
from app.config import settings


# Doctor data with department mapping
DOCTORS_DATA = [
    {
        "name": "Dr. Md. Foyezul Haque Sarkar",
        "email": "",
        "phone": "",
        "specialty": "Nephrology (Kidney Medicine)",
        "department_name": "Hematology",  # Will be mapped to actual department
        "image_url": "/public/doctors/Dr Foyezul Haque Sarker_Photo.png",
        "bio": "Physician specialized in kidney disease, diabetes, hypertension, and internal medicine. Works at National Kidney Disease Hospital, Shyamoli, Dhaka. Provides comprehensive care for chronic kidney disease and related complications.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "degrees": ["MBBS", "CCD (Medicine)", "MD (Nephrology) – Phase B"],
            "workplace": "National Kidney Disease Hospital, Shyamoli, Dhaka",
            "visiting_schedule": [
                {"day": "Thursday", "time": "3:00 PM - 7:00 PM"}
            ],
            "treats": [
                "Kidney disease",
                "Diabetes",
                "High blood pressure",
                "Breathing difficulty",
                "Loss of appetite",
                "Excessive thirst",
                "Reduced or excessive urination",
                "Body itching and weakness"
            ]
        }
    },
    {
        "name": "Dr. Ahmed Rubaiyat",
        "email": "",
        "phone": "",
        "specialty": "Pediatrics (Child & Adolescent Health)",
        "department_name": "Pediatrics",
        "image_url": "/public/doctors/Dr Ahmed Robayet.png",
        "bio": "Pediatric specialist treating newborns, children, and adolescents. Affiliated with Dhaka Medical College & Hospital.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "degrees": ["MBBS", "PGT (Pediatrics)", "FCPS (Pediatric Cardiology)"],
            "workplace": "Dhaka Medical College & Hospital",
            "visiting_schedule": [
                {"day": "Saturday", "time": "10:00 AM - 5:00 PM"},
                {"day": "Tuesday", "time": "3:00 PM - 6:00 PM"}
            ],
            "treats": [
                "Fever and infections",
                "Cold, cough, pneumonia",
                "Asthma",
                "Abdominal pain",
                "Vomiting and diarrhea",
                "Growth and nutrition problems",
                "Developmental delays",
                "All newborn and child health issues"
            ]
        }
    },
    {
        "name": "Dr. Maksuda Akter",
        "email": "",
        "phone": "",
        "specialty": "Obstetrics & Gynecology",
        "department_name": "Obstetrics and Gynecology",
        "image_url": "/public/doctors/Dr Maksuda Akter_Photo.png",
        "bio": "Gynecologist and obstetrician providing maternity care, pregnancy monitoring, and women's health services.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "degrees": ["MBBS", "MCGP (Gynecology & Obstetrics)", "CMU (Ultrasound)", "CCD (BIRDEM)"],
            "visiting_schedule": [
                {"day": "Daily", "time": "10:00 AM - 6:00 PM"}
            ],
            "treats": [
                "Pregnancy care",
                "Normal delivery",
                "Gestational diabetes",
                "Infertility",
                "Gynecological disorders",
                "Women's cancer screening"
            ]
        }
    },
    {
        "name": "Dr. Md. Rafiqul Bari",
        "email": "",
        "phone": "",
        "specialty": "Neurology (Neuro Medicine)",
        "department_name": "Neurology",
        "image_url": "/public/doctors/Dr Rafiul Bari_Photo.png",
        "bio": "Neuro-medicine specialist treating neurological and systemic medical conditions. Assistant Registrar at Dhaka Medical College Hospital.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "degrees": ["MBBS", "BCS (Health)", "FCPS (Neuro Medicine)"],
            "position": "Assistant Registrar (Neuro Medicine)",
            "workplace": "Dhaka Medical College & Hospital",
            "visiting_schedule": [
                {"day": "Thursday", "time": "3:00 PM - 6:00 PM"}
            ],
            "treats": [
                "Stroke",
                "Seizures",
                "Coma",
                "Headache",
                "Diabetes-related nerve problems",
                "Kidney-related neurological symptoms"
            ]
        }
    },
    {
        "name": "Dr. Arman Ullah Chowdhury",
        "email": "",
        "phone": "",
        "specialty": "Neurology (Neuro Medicine)",
        "department_name": "Neurology",
        "image_url": "/public/doctors/Dr Arman Ullah Choudhury_Photo.png",
        "bio": "Registrar in Neuro Medicine treating neurological, diabetic, cardiac, and rheumatologic disorders.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "degrees": ["MBBS", "BCS (Health)", "CCD (BIRDEM)", "FCPS (Medicine)"],
            "position": "Registrar (Neuro Medicine)",
            "workplace": "Manikganj Medical College & Hospital",
            "visiting_schedule": [
                {"day": "Saturday", "time": "3:00 PM - 6:00 PM"}
            ],
            "treats": [
                "Stroke",
                "Headache",
                "Seizures",
                "Diabetes",
                "Heart disease",
                "Thyroid disorders",
                "Kidney-related neurological issues"
            ]
        }
    },
    {
        "name": "Dr. Rumana Farzana",
        "email": "",
        "phone": "",
        "specialty": "Pediatrics (Child & Newborn Health)",
        "department_name": "Pediatrics",
        "image_url": "/public/doctors/Dr Rumana Farzana.png",
        "bio": "Assistant Professor of Pediatrics providing specialized care for newborns and children. Faculty member at Ad-din Women's Medical College.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "degrees": ["MBBS (DMC)", "MD (Pediatrics)"],
            "position": "Assistant Professor (Pediatrics)",
            "workplace": "Ad-din Women's Medical College, Dhaka",
            "visiting_schedule": [
                {"day": "Sunday", "time": "2:00 PM - 5:00 PM"},
                {"day": "Wednesday", "time": "10:00 AM - 5:00 PM"}
            ],
            "treats": [
                "Newborn care",
                "Childhood infections",
                "Asthma",
                "Nutrition and growth issues",
                "Developmental delays",
                "All pediatric medical conditions"
            ]
        }
    },
    {
        "name": "Dr. Md. Asraful Amin",
        "email": "",
        "phone": "",
        "specialty": "Family Medicine / Neuro Medicine",
        "department_name": "Neurology",
        "image_url": "/public/doctors/Dr Ashraful Amin (2).png",
        "bio": "Family medicine physician with expertise in neuro medicine, diabetes, rheumatology, and chronic diseases. Assistant Registrar at Army Medical College, CMH Cumilla.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "degrees": [
                "MBBS",
                "FCGP (Family Medicine)",
                "CCD (Diabetes)",
                "DOC (Dermatology & Venereology)"
            ],
            "position": "Assistant Registrar",
            "workplace": "Army Medical College, CMH Cumilla",
            "visiting_schedule": [
                {"day": "Tuesday", "time": "10:00 AM - 5:00 PM"}
            ],
            "treats": [
                "Neurological disorders",
                "Stroke and paralysis",
                "Diabetes",
                "Heart disease",
                "Asthma",
                "Kidney and liver disease",
                "Skin and sexual health problems",
                "Child and adolescent diseases"
            ]
        }
    },
    {
        "name": "Dr. Limon Chandra Dhar",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Urology • General & Laparoscopic Surgery",
        "department_name": "Urology",
        "image_url": "/public/doctors/Dr Limon Chandro Dhor_photo_01.png",
        "bio": "Consultant urologist; performs general and laparoscopic surgical procedures. Affiliation listed: Dhaka Medical College Hospital.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Urology",
            "degrees": ["MBBS", "BCS (Health)", "FCPS (Surgery)", "MS (Urology)"],
            "designation": "Consultant (Urology), Dhaka Medical College Hospital",
            "visiting_schedule": [{"day": "Monday", "time": "3:00 PM - 6:00 PM"}],
            "treats": [
                "All abdominal surgeries",
                "Kidney/urinary stones and stone-related problems",
                "Kidney & urinary bladder diseases",
                "Hernia",
                "Testicular/scrotal problems",
                "Genital diseases including hydrocele",
                "Breast problems in women",
                "Gynecomastia (male breast enlargement)",
                "Cancer care & tumor surgery (as applicable)"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. Md. Shamin Mia",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Medicine • Diabetes • Hypertension • Rheumatology • Cardiology",
        "department_name": "Cardiology",
        "image_url": "/public/doctors/Dr M Shamim Miah (1).png",
        "bio": "Consultant physician focused on diabetes, blood pressure, chest and heart-related diseases (as listed in the poster).",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Medicine/Cardiology",
            "degrees": ["MBBS (DU)", "CCD (BIRDEM)", "D-CARD (Cardiology) (as listed)"],
            "designation": "Consultant (Cardiology) & Ex-Assistant Registrar (Cardiology) — (as listed)",
            "visiting_schedule": [
                {"day": "Wednesday", "time": "10:00 AM - 5:00 PM"},
                {"day": "Friday", "time": "10:00 AM - 5:00 PM"}
            ],
            "treats": [
                "Hypertension (including uncontrolled/high BP)",
                "Chest pain & suspected heart attack",
                "Heart failure/shortness of breath",
                "Palpitations/arrhythmia",
                "High cholesterol",
                "Diabetes management & complications",
                "Rheumatic (joint/body) pain",
                "ECG/heart check-up follow-up (as applicable)"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. Md. Nazrul Islam Jalim",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Orthopedics • Trauma & Reconstructive Surgery",
        "department_name": "Orthopedics",
        "image_url": "/public/doctors/Dr Md Nazrul Islam Dalim_Photo.png",
        "bio": "Orthopedic specialist and trauma/reconstructive surgeon; workplace listed: Pangu Hospital, Shyamoli, Dhaka.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Orthopedics",
            "degrees": [
                "MBBS",
                "BCS (Health)",
                "D-Ortho (Orthopedic Surgery)",
                "Advanced Pain Management (India)",
                "Advanced Wound Management (Ireland)",
                "Member, AO Trauma (Switzerland)"
            ],
            "designation": "Trauma & Reconstructive Surgeon, Pangu Hospital, Shyamoli, Dhaka",
            "visiting_schedule": [
                {"day": "Sunday", "time": "3:00 PM - 6:00 PM"},
                {"day": "Wednesday", "time": "3:00 PM - 6:00 PM"}
            ],
            "treats": [
                "Bone, neck, back and joint pain",
                "Fractures & trauma care",
                "Arthritis and sports injuries",
                "Wound/ulcer care including diabetic foot",
                "Plaster/casting and postoperative follow-up"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. Muntasir Al Maruf",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "ENT • Head & Neck Surgery",
        "department_name": "Neurology",  # ENT not in list, mapping to closest
        "image_url": "/public/doctors/Dr Muntasir Al Maruf_Photo_01.png",
        "bio": "ENT specialist and Head-Neck surgeon; affiliation listed: Dhaka Medical College & Hospital.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "ENT",
            "degrees": ["MBBS (as listed)", "MS (ENT)", "FCPS (ENT) (as listed)"],
            "designation": "ENT & Head-Neck Surgeon, Dhaka Medical College & Hospital",
            "visiting_schedule": [
                {"day": "Sunday", "time": "1:00 PM - 5:00 PM"},
                {"day": "Tuesday", "time": "1:00 PM - 5:00 PM"},
                {"day": "Thursday", "time": "1:00 PM - 5:00 PM"}
            ],
            "treats": [
                "Tonsillitis",
                "Nasal blockage & nasal polyps/allergy",
                "Sinus disease and sinus surgery",
                "Ear microsurgery",
                "Ear discharge & eardrum perforation surgery",
                "Thyroid/voice-related ENT issues (as applicable)",
                "Throat tumors/cancer evaluation",
                "Hearing loss, tinnitus and vertigo",
                "Speech delay evaluation in children",
                "Endoscopic (camera) diagnosis for nose, ear and throat"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. Anik Poddar",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Nephrology • Medicine • Diabetes • Gastroenterology (as listed)",
        "department_name": "Hematology",
        "image_url": "/public/doctors/Dr Anik Puddar_Photo (1).png",
        "bio": "Consultant nephrologist; manages kidney disease along with diabetes and common medical/gastrointestinal problems.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Nephrology",
            "degrees": ["MBBS", "BCS (Health)", "MD (Nephrology)", "DMSc", "MCPS (USA) (as listed)", "PGDT (Gastroenterology)"],
            "designation": "Consultant (Nephrology)",
            "visiting_schedule": [{"day": "Saturday", "time": "3:00 PM - 6:00 PM"}],
            "treats": [
                "Kidney disease and kidney-related symptoms",
                "Diabetes management",
                "Gastric/acid reflux/ulcer",
                "Liver disease & jaundice",
                "Chronic swelling/edema",
                "High blood pressure",
                "Urinary symptoms (low urine output, frequent/burning urination)",
                "General internal medicine issues"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. Md. Mohi Uddin",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Medicine • Diabetes • Hypertension • Thyroid • Rheumatology • Chest Diseases",
        "department_name": "Cardiology",
        "image_url": "/public/doctors/Dr Md Mohi Uddin.png",
        "bio": "Consultant physician (Medicine) at Dhaka Medical College Hospital (as listed); treats diabetes, thyroid disorders, hypertension and common internal medicine problems.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Medicine",
            "degrees": ["MBBS", "BCS (Health)", "FCPS (Medicine)", "Member, American College of Physicians (as listed)"],
            "designation": "Consultant (Medicine), Dhaka Medical College & Hospital",
            "visiting_schedule": [
                {"day": "Wednesday", "time": "10:00 AM - 5:00 PM"},
                {"day": "Monday", "time": "3:00 PM - 7:00 PM"}
            ],
            "treats": [
                "Diabetes, thyroid & hormonal problems",
                "Hypertension",
                "Chest pain and breathing problems",
                "Gastric and liver problems",
                "Rheumatic (joint/body) pain",
                "Fever, cough/cold and infections",
                "Migraine/headache",
                "Sleep problems/anxiety (as applicable)"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. Md. Asad Ullah",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Pediatrics • Neonatology",
        "department_name": "Pediatrics",
        "image_url": "/public/doctors/Dr Asadullah_01.png",
        "bio": "Physician for newborns and children; workplace listed: Shishu-Matu Health Institute, Matuaile, Dhaka.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Pediatrics/Neonatology",
            "degrees": ["MBBS", "FCPS (Neonatology) (as listed)", "MD (Pediatrics) (as listed)"],
            "designation": "Child & Newborn Specialist, Shishu-Matu Health Institute, Matuaile, Dhaka",
            "visiting_schedule": [
                {"day": "Monday", "time": "10:00 AM - 5:00 PM"},
                {"day": "Thursday", "time": "10:00 AM - 5:00 PM"}
            ],
            "treats": [
                "Fever, cold and cough",
                "Pneumonia/respiratory infections",
                "Sore throat/tonsillitis/asthma",
                "Vomiting, diarrhea and dehydration",
                "Urinary problems in children",
                "Food allergy and poor appetite",
                "Malnutrition/growth issues",
                "Child physical & mental development concerns",
                "Any newborn and child health problems"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. M. S. Alam Sikder",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Ophthalmology • Phaco (Cataract) Surgery",
        "department_name": "Ophthalmology",
        "image_url": "/public/doctors/Dr M S Alam Sikder_photo.png",
        "bio": "Eye specialist and phaco surgeon; Senior Consultant & Head of Eye Department at Narayanganj Diabetes Hospital (as listed).",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Ophthalmology",
            "degrees": ["MBBS", "DO (DU)", "IOL & Phaco Surgery Training (as listed)"],
            "designation": "Senior Consultant & Department Head (Ophthalmology), Narayanganj Diabetes Hospital",
            "visiting_schedule": [{"day": "Wednesday", "time": "10:00 AM - 6:00 PM"}],
            "treats": [
                "Red eye, watery eyes and allergy",
                "Low vision (near/far), eye strain and headache",
                "Eye injury/foreign body",
                "Cataract (phaco/IOL)",
                "Pterygium and other ocular surface problems",
                "Glaucoma evaluation",
                "Children's eye problems",
                "IOP (eye pressure) measurement",
                "SPT test (as listed)"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. Sanif Hossain",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Family Medicine • Internal Medicine • Diabetes • Mother & Child Care • Skin & Sexual Health • Asthma",
        "department_name": "Pediatrics",
        "image_url": "/public/doctors/Dr Sanif Hossain_Photo.png",
        "bio": "Family medicine physician providing broad primary care including adult medicine, diabetes, mother & child care, skin/sexual health and asthma (as listed).",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Family Medicine",
            "degrees": ["MBBS", "CCCD (BIRDEM)", "MCGP (Family Medicine)", "CMUED (Asthma)", "CCT (Medicine)"],
            "designation": "Physician (Family Medicine)",
            "visiting_schedule": [{"day": "Daily", "time": "10:00 AM - 6:00 PM"}],
            "treats": [
                "General medicine",
                "Diabetes care",
                "Mother & child care",
                "Rheumatism (joint/body pain)",
                "Skin and sexual health problems",
                "Asthma and breathing issues"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
    {
        "name": "Dr. Md. Faruk Rahman Majumdar",
        "email": "",
        "phone": "01334 92 77 23",
        "specialty": "Medicine • Diabetes • Hypertension • Rheumatology • Cardiology",
        "department_name": "Cardiology",
        "image_url": "/public/doctors/Dr Md Faroque Rahman Majumder_photo.png",
        "bio": "Consultant doctor focused on medicine/diabetes/hypertension/rheumatism and heart disease (as listed). Affiliation listed: Dhaka Medical College Hospital.",
        "experience_years": 0,
        "is_available": True,
        "profile_data": {
            "department": "Medicine/Cardiology",
            "degrees": ["MBBS", "FCPS (Medicine)", "FCGP", "D-CARD (Cardiology)", "NDOM (CCU) (as listed)", "NDOPROG (Rheumatology) (as listed)"],
            "designation": "Consultant (Cardiology), Dhaka Medical College & Hospital",
            "visiting_schedule": [{"day": "Sunday", "time": "10:00 AM - 8:00 PM"}],
            "treats": [
                "Hypertension (including uncontrolled/high BP)",
                "Chest pain and heart disease follow-up",
                "Rheumatism/joint pains",
                "Diabetes management",
                "Heart failure/shortness of breath",
                "ECG/heart monitoring follow-up (as applicable)"
            ],
            "contacts": {
                "hospital": "Najmul Modern Hospital",
                "address": "Moni-Mukta & Bymok Complex, Dautkandi Toll Plaza, Dautkandi, Cumilla",
                "hotline": "01334 92 77 22",
                "serial_phone": "01334 92 77 23",
                "whatsapp": "01711 947418",
                "facebook": "NMHDK"
            }
        }
    },
]


async def seed_doctors():
    """Seed doctors into the database"""
    
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        future=True
    )
    
    # Create session factory
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    try:
        async with async_session() as session:
            print("🔍 Checking existing doctors...")
            
            # Check if doctors already exist
            result = await session.execute(select(Doctor))
            existing_doctors = result.scalars().all()
            
            if existing_doctors:
                print(f"⚠️  Found {len(existing_doctors)} existing doctors")
                print("Existing doctors:")
                for doctor in existing_doctors:
                    print(f"  - {doctor.name}")
                
                response = input("\n❓ Do you want to clear and reseed? (yes/no): ").strip().lower()
                if response == "yes":
                    print("🗑️  Deleting existing doctors...")
                    await session.query(Doctor).delete()
                    await session.commit()
                    print("✅ Deleted existing doctors")
                else:
                    print("⏭️  Skipping seed operation")
                    return
            
            print(f"\n📝 Seeding {len(DOCTORS_DATA)} doctors...")
            
            # Create doctor objects with department mapping
            doctors = []
            failed_doctors = []
            
            for doctor_data in DOCTORS_DATA:
                try:
                    # Get department by name
                    dept_result = await session.execute(
                        select(Department).where(
                            Department.name == doctor_data["department_name"]
                        )
                    )
                    department = dept_result.scalar_one_or_none()
                    
                    if not department:
                        print(f"⚠️  Department '{doctor_data['department_name']}' not found for {doctor_data['name']}")
                        failed_doctors.append(doctor_data['name'])
                        continue
                    
                    doctor = Doctor(
                        name=doctor_data["name"],
                        email=doctor_data.get("email", ""),
                        phone=doctor_data.get("phone", ""),
                        specialty=doctor_data["specialty"],
                        department_id=department.id,
                        image_url=doctor_data.get("image_url", ""),
                        bio=doctor_data.get("bio", ""),
                        experience_years=doctor_data.get("experience_years", 0),
                        is_available=doctor_data.get("is_available", True),
                        profile_data=doctor_data.get("profile_data", {}),
                        is_active=True
                    )
                    doctors.append(doctor)
                except Exception as e:
                    print(f"❌ Error processing {doctor_data['name']}: {str(e)}")
                    failed_doctors.append(doctor_data['name'])
            
            if not doctors:
                print("❌ No doctors could be seeded!")
                return
            
            # Add all doctors to session
            session.add_all(doctors)
            
            # Commit the transaction
            await session.commit()
            
            print(f"✅ Successfully seeded {len(doctors)} doctors!")
            print("\n📋 Seeded Doctors:")
            for i, doctor in enumerate(doctors, 1):
                print(f"  {i}. {doctor.name} - {doctor.specialty}")
            
            if failed_doctors:
                print(f"\n⚠️  Failed to seed {len(failed_doctors)} doctors:")
                for doctor_name in failed_doctors:
                    print(f"  - {doctor_name}")
            
    except Exception as e:
        print(f"❌ Error seeding doctors: {str(e)}")
        raise
    finally:
        await engine.dispose()


async def main():
    """Main entry point"""
    print("=" * 60)
    print("🏥 Hospital Doctor Seed Script")
    print("=" * 60)
    print(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Unknown'}")
    print("=" * 60 + "\n")
    
    await seed_doctors()
    
    print("\n" + "=" * 60)
    print("✨ Seed operation completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta
NB_REGIONS = 5
SCHOOLS_PER_REGION = {
    "Casablanca-Settat": 7,
    "Rabat-Salé-Kénitra": 6,
    "Tanger-Tétouan-Al Hoceïma": 5,
    "Fès-Meknès": 4,
    "Marrakech-Safi": 3
}

CLASS_SIZE_BY_REGION = {
    "Casablanca-Settat": (25, 35),
    "Rabat-Salé-Kénitra": (28, 38),
    "Tanger-Tétouan-Al Hoceïma": (30, 40),
    "Fès-Meknès": (32, 42),
    "Marrakech-Safi": (35, 45)
}

CLASSES_PER_SCHOOL = {
    "Casablanca-Settat": (15, 25),
    "Rabat-Salé-Kénitra": (12, 20),
    "Tanger-Tétouan-Al Hoceïma": (10, 18),
    "Fès-Meknès": (8, 15),
    "Marrakech-Safi": (6, 12)
}

NB_TEACHERS = 120

SUBJECTS = ["Mathématiques", "Physique", "SVT", "Français", "Philosophie", "Économie"]
LEVELS = ["Tronc Commun", "1ère Bac", "2ème Bac"]
STREAMS = ["Sciences", "Lettres", "Économie"]
ABSENCE_PROFILES = {
    "Casablanca-Settat": {
        "faible": 0.80, "moyen": 0.15, "eleve": 0.05,
        "taux_base": 0.03
    },
    "Rabat-Salé-Kénitra": {
        "faible": 0.75, "moyen": 0.18, "eleve": 0.07,
        "taux_base": 0.04
    },
    "Tanger-Tétouan-Al Hoceïma": {
        "faible": 0.65, "moyen": 0.25, "eleve": 0.10,
        "taux_base": 0.06
    },
    "Fès-Meknès": {
        "faible": 0.60, "moyen": 0.25, "eleve": 0.15,
        "taux_base": 0.08
    },
    "Marrakech-Safi": {
        "faible": 0.50, "moyen": 0.30, "eleve": 0.20,
        "taux_base": 0.12
    }
}

PERFORMANCE_BY_REGION = {
    "Casablanca-Settat": (13, 18),
    "Rabat-Salé-Kénitra": (12, 17),
    "Tanger-Tétouan-Al Hoceïma": (10, 15),
    "Fès-Meknès": (9, 14),
    "Marrakech-Safi": (7, 13)
}

OUTPUT_DIR = "data_raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)
np.random.seed(42)
moroccan_regions = [
    {"name": "Casablanca-Settat", "socio_economic_index": 0.95, "urbanization_rate": 0.95},
    {"name": "Rabat-Salé-Kénitra", "socio_economic_index": 0.85, "urbanization_rate": 0.88},
    {"name": "Tanger-Tétouan-Al Hoceïma", "socio_economic_index": 0.65, "urbanization_rate": 0.68},
    {"name": "Fès-Meknès", "socio_economic_index": 0.45, "urbanization_rate": 0.50},
    {"name": "Marrakech-Safi", "socio_economic_index": 0.35, "urbanization_rate": 0.40}
]

regions = pd.DataFrame({
    "region_id": range(1, NB_REGIONS + 1),
    "region_name": [r["name"] for r in moroccan_regions],
    "socio_economic_index": [r["socio_economic_index"] for r in moroccan_regions],
    "urbanization_rate": [r["urbanization_rate"] for r in moroccan_regions]
})
school_names_by_region = {
    "Casablanca-Settat": [
        {"name": "Lycée Lyautey", "city": "Casablanca"},
        {"name": "Lycée Mohammed VI", "city": "Casablanca"},
        {"name": "Lycée Oum Banine", "city": "Settat"},
        {"name": "Lycée Al Wahda", "city": "Casablanca"},
        {"name": "Lycée Ghandi", "city": "Casablanca"},
        {"name": "Lycée Anfa", "city": "Casablanca"},
        {"name": "Lycée Maârif", "city": "Casablanca"}
    ],
    "Rabat-Salé-Kénitra": [
        {"name": "Lycée Descartes", "city": "Rabat"},
        {"name": "Lycée Moulay Youssef", "city": "Rabat"},
        {"name": "Lycée Ibn Sina", "city": "Salé"},
        {"name": "Lycée Al Massira", "city": "Kénitra"},
        {"name": "Lycée Technique", "city": "Rabat"},
        {"name": "Lycée Hassan II", "city": "Rabat"}
    ],
    "Tanger-Tétouan-Al Hoceïma": [
        {"name": "Lycée Regnault", "city": "Tanger"},
        {"name": "Lycée Ibn Batouta", "city": "Tanger"},
        {"name": "Lycée Moulay El Hassan", "city": "Tétouan"},
        {"name": "Lycée Al Andalus", "city": "Tanger"},
        {"name": "Lycée Mohammed Daoud", "city": "Tétouan"}
    ],
    "Fès-Meknès": [
        {"name": "Lycée Mohammed V", "city": "Fès"},
        {"name": "Lycée Hassan II", "city": "Meknès"},
        {"name": "Lycée Al Khawarizmi", "city": "Fès"},
        {"name": "Lycée Ibn Khaldoun", "city": "Meknès"}
    ],
    "Marrakech-Safi": [
        {"name": "Lycée Ibn Abbad", "city": "Marrakech"},
        {"name": "Lycée Victor Hugo", "city": "Marrakech"},
        {"name": "Lycée Al Qods", "city": "Safi"}
    ]
}
schools = []
school_id = 1
for _, region in regions.iterrows():
    region_name = region["region_name"]
    nb_schools = SCHOOLS_PER_REGION[region_name]
    region_schools = school_names_by_region[region_name]
    
    for i in range(nb_schools):
        school_info = region_schools[i % len(region_schools)]

        base_perf = region["socio_economic_index"]
        school_performance = np.clip(
            np.random.normal(base_perf, 0.08),
            base_perf - 0.15,
            min(1.0, base_perf + 0.10)
        )
        
        schools.append([
            school_id,
            school_info["name"] + (f" {i+1}" if i >= len(region_schools) else ""),
            school_info["city"],
            region["region_id"],
            random.choice(["Public", "Privé"]),
            school_performance,
            random.randint(300, 1500)
        ])
        school_id += 1

schools = pd.DataFrame(schools, columns=[
    "school_id", "school_name", "city", "region_id", "type", 
    "performance_index", "capacity"
])

print(f"{len(schools)} établissements créés (variation régionale)")
for region_name, count in SCHOOLS_PER_REGION.items():
    region_id = regions[regions["region_name"] == region_name]["region_id"].values[0]
    actual = len(schools[schools["region_id"] == region_id])
    print(f"   - {region_name}: {actual} écoles")
classes = []
class_id = 1
for _, school in schools.iterrows():
    region_name = regions[regions["region_id"] == school["region_id"]]["region_name"].values[0]
    min_classes, max_classes = CLASSES_PER_SCHOOL[region_name]
    nb_classes = random.randint(min_classes, max_classes)
    
    for i in range(nb_classes):
        classes.append([
            class_id,
            f"Classe {class_id}",
            random.choice(LEVELS),
            random.choice(STREAMS),
            school["school_id"]
        ])
        class_id += 1

classes = pd.DataFrame(classes, columns=[
    "class_id", "class_name", "level", "stream", "school_id"
])

print(f"{len(classes)} classes créées")
first_names = [
    "Yassine", "Sara", "Hamza", "Imane", "Omar", "Khadija", "Amina", "Mehdi",
    "Youssef", "Salma", "Aya", "Adam", "Zineb", "Anas", "Fatima", "Ayoub",
    "Meriem", "Ilias", "Nadia", "Karim", "Hafsa", "Rachid", "Asmae", "Bilal",
    "Hiba", "Saad", "Laila", "Ismail", "Ghita", "Othmane", "Sanaa", "Jamal",
    "Houda", "Tarik", "Samira", "Walid", "Nawal", "Abdelaziz", "Karima", "Hicham"
]

last_names = [
    "El Amrani", "Benali", "Chafiq", "Rahmani", "Ait Taleb", "Kabbaj", "Berrada",
    "Idrissi", "Bennani", "Fassi", "Alaoui", "Zahraoui", "Tazi", "El Ouardi",
    "Benhaddou", "Chraibi", "Lahlou", "Filali", "Bouazza", "Kadiri", "Naciri"
]
print("Génération des élèves avec profils régionaux différenciés...")
students = []
student_id = 1

for _, cls in classes.iterrows():
    school_info = schools[schools["school_id"] == cls["school_id"]].iloc[0]
    region_name = regions[regions["region_id"] == school_info["region_id"]]["region_name"].values[0]

    min_size, max_size = CLASS_SIZE_BY_REGION[region_name]
    nb_students = random.randint(min_size, max_size)

    absence_profile = ABSENCE_PROFILES[region_name]

    profil_choices = (
        ['faible'] * int(absence_profile['faible'] * 100) +
        ['moyen'] * int(absence_profile['moyen'] * 100) +
        ['eleve'] * int(absence_profile['eleve'] * 100)
    )
    
    for _ in range(nb_students):
        profil_absence = random.choice(profil_choices)

        base_rate = absence_profile['taux_base']
        
        if profil_absence == 'faible':
            absence_rate = np.random.uniform(base_rate * 0.2, base_rate * 0.8)
        elif profil_absence == 'moyen':
            absence_rate = np.random.uniform(base_rate * 1.2, base_rate * 2.0)
        else:
            absence_rate = np.random.uniform(base_rate * 2.5, base_rate * 4.0)

        if profil_absence == 'faible':
            dropout_risk = np.random.uniform(0.01, 0.10)
        elif profil_absence == 'moyen':
            dropout_risk = np.random.uniform(0.15, 0.35)
        else:
            dropout_risk = np.random.uniform(0.40, 0.75)

        dropout_risk *= (1.5 - school_info["performance_index"] * 0.5)
        dropout_risk = min(dropout_risk, 0.95)
        
        students.append([
            student_id,
            random.choice(first_names),
            random.choice(last_names),
            random.choice(["M", "F"]),
            pd.to_datetime(np.random.choice(pd.date_range("2005-01-01", "2008-12-31"))),
            cls["class_id"],
            dropout_risk,
            absence_rate,
            profil_absence,
            region_name
        ])
        student_id += 1

students = pd.DataFrame(students, columns=[
    "student_id", "first_name", "last_name", "gender", "birth_date", 
    "class_id", "dropout_risk_score", "target_absence_rate", 
    "profil_absence", "region_name"
])

print(f"{len(students):,} élèves générés")
print("\nRÉPARTITION PAR RÉGION:")
for region_name in regions["region_name"]:
    count = len(students[students["region_name"] == region_name])
    avg_absence = students[students["region_name"] == region_name]["target_absence_rate"].mean() * 100
    print(f"   - {region_name}: {count:,} élèves (absence moy: {avg_absence:.1f}%)")
subject_coefficients = {
    "Mathématiques": 7,
    "Physique": 7,
    "SVT": 5,
    "Français": 4,
    "Philosophie": 3,
    "Économie": 5
}

subjects = pd.DataFrame({
    "subject_id": range(1, len(SUBJECTS) + 1),
    "subject_name": SUBJECTS,
    "coefficient": [subject_coefficients[s] for s in SUBJECTS]
})
teacher_assignments = []
assignment_id = 1

for _, school in schools.iterrows():
    for subject_id in subjects["subject_id"]:
        teacher_id = random.randint(1, NB_TEACHERS)
        teacher_assignments.append([
            assignment_id,
            teacher_id,
            subject_id,
            school["school_id"]
        ])
        assignment_id += 1

teacher_assignments = pd.DataFrame(teacher_assignments, columns=[
    "assignment_id", "teacher_id", "subject_id", "school_id"
])

teachers = pd.DataFrame({
    "teacher_id": range(1, NB_TEACHERS + 1),
    "name": [f"Prof {i}" for i in range(1, NB_TEACHERS + 1)],
    "experience_years": np.random.randint(1, 30, NB_TEACHERS),
    "teaching_quality_score": np.random.uniform(0.5, 1.0, NB_TEACHERS)
})
dates = pd.date_range(start="2023-09-01", end="2024-06-30")
time = pd.DataFrame({
    "time_id": range(1, len(dates) + 1),
    "date": dates
})
time["year"] = time["date"].dt.year
time["month"] = time["date"].dt.month
time["week"] = time["date"].dt.isocalendar().week
time["day_of_week"] = time["date"].dt.dayofweek
time["is_weekend"] = time["day_of_week"].isin([5, 6])

def assign_term(month):
    if month in [9, 10, 11, 12]:
        return "T1"
    elif month in [1, 2, 3, 4, 5, 6]:
        return "T2"
    else:
        return "Vacances"

time["term"] = time["month"].apply(assign_term)
MONTHLY_ABSENCE_FACTOR = {
    9: 0.7,
    10: 0.9,
    11: 1.1,
    12: 1.3,
    1: 1.4,
    2: 1.5,
    3: 1.2,
    4: 1.0,
    5: 0.9,
    6: 1.1
}
print("Génération des notes avec disparités régionales...")
grades = []
grade_id = 1

for _, student in students.iterrows():
    region_name = student["region_name"]
    perf_min, perf_max = PERFORMANCE_BY_REGION[region_name]

    if student["profil_absence"] == 'faible':
        base_performance = np.random.uniform(perf_min + 2, perf_max)
    elif student["profil_absence"] == 'moyen':
        base_performance = np.random.uniform(perf_min - 1, perf_max - 3)
    else:
        base_performance = np.random.uniform(perf_min - 3, perf_max - 5)
    
    base_performance = np.clip(base_performance, 0, 20)
    
    for _, subject in subjects.iterrows():
        class_info = classes[classes["class_id"] == student["class_id"]].iloc[0]
        school_id = class_info["school_id"]
        
        teacher_assignment = teacher_assignments[
            (teacher_assignments["subject_id"] == subject["subject_id"]) & 
            (teacher_assignments["school_id"] == school_id)
        ]
        
        if len(teacher_assignment) == 0:
            continue

        teacher_id = teacher_assignment.iloc[0]["teacher_id"]
        
        for term in ["T1", "T2"]:
            if term == "T2":
                score = base_performance + np.random.uniform(-1.5, 2.0)
            else:
                score = base_performance + np.random.uniform(-1.0, 1.0)
            
            score = np.clip(score, 0, 20)
            score = round(score, 2)
            
            grades.append([
                grade_id,
                student["student_id"],
                subject["subject_id"],
                teacher_id,
                student["class_id"],
                term,
                2024,
                score,
                "Validé" if score >= 10 else "Échec"
            ])
            grade_id += 1

grades = pd.DataFrame(grades, columns=[
    "grade_id", "student_id", "subject_id", "teacher_id", 
    "class_id", "term", "year", "score", "status"
])

print(f"{len(grades):,} notes générées")
print("Génération des présences avec variations mensuelles...")
attendance = []
attendance_id = 1

school_days = time[~time["is_weekend"]]["date"].values[:180]

for idx, student in students.iterrows():
    if idx % 2000 == 0:
        print(f"   {idx}/{len(students)} élèves")
    
    class_info = classes[classes["class_id"] == student["class_id"]].iloc[0]
    school_id = class_info["school_id"]
    region_id = schools[schools["school_id"] == school_id]["region_id"].values[0]
    
    absence_dates = set()

    for day in school_days:
        day_ts = pd.Timestamp(day)
        month = day_ts.month

        monthly_factor = MONTHLY_ABSENCE_FACTOR.get(month, 1.0)
        prob_absent = student["target_absence_rate"] * monthly_factor
        
        if random.random() < prob_absent:
            absence_dates.add(day_ts)
    
    for day in school_days:
        is_absent = pd.Timestamp(day) in absence_dates
        subject_id = random.choice(subjects["subject_id"].values)
        
        teacher_assignment = teacher_assignments[
            (teacher_assignments["subject_id"] == subject_id) & 
            (teacher_assignments["school_id"] == school_id)
        ]
        
        if len(teacher_assignment) == 0:
            continue
        
        teacher_id = teacher_assignment.iloc[0]["teacher_id"]
        
        if is_absent:
            is_justified = random.random() < 0.50
            status = "Absent Justifié" if is_justified else "Absent Non Justifié"
            reason = random.choice(["Maladie", "Familial", "Transport", "Non spécifié"]) if is_justified else "Non justifié"
        else:
            status = "Présent"
            reason = None
        
        attendance.append([
            attendance_id,
            student["student_id"],
            student["class_id"],
            school_id,
            region_id,
            subject_id,
            teacher_id,
            pd.Timestamp(day),
            status,
            reason
        ])
        attendance_id += 1

attendance = pd.DataFrame(attendance, columns=[
    "attendance_id", "student_id", "class_id", "school_id", "region_id",
    "subject_id", "teacher_id", "date", "status", "reason"
])

print(f"{len(attendance):,} enregistrements")
print("Calcul des métriques...")
student_metrics = []

for _, student in students.iterrows():
    student_attendance = attendance[attendance["student_id"] == student["student_id"]]
    student_grades = grades[grades["student_id"] == student["student_id"]]
    
    total_days = len(student_attendance)
    absent_days = len(student_attendance[student_attendance["status"].str.contains("Absent")])
    unjustified = len(student_attendance[student_attendance["status"] == "Absent Non Justifié"])
    
    absence_rate = absent_days / total_days if total_days > 0 else 0
    avg_score = student_grades["score"].mean()
    
    if student["dropout_risk_score"] > 0.4 or (absence_rate > 0.15 and avg_score < 8):
        risk_level = "Élevé"
    elif student["dropout_risk_score"] > 0.20 or (absence_rate > 0.08 or avg_score < 10):
        risk_level = "Moyen"
    else:
        risk_level = "Faible"
    
    student_metrics.append([
        student["student_id"],
        student["class_id"],
        total_days,
        absent_days,
        unjustified,
        absence_rate,
        avg_score,
        risk_level,
        student["dropout_risk_score"]
    ])

student_metrics = pd.DataFrame(student_metrics, columns=[
    "student_id", "class_id", "total_school_days", "absent_days",
    "unjustified_absences", "absence_rate", "average_score",
    "risk_level", "dropout_risk_score"
])

print("Export des fichiers...")

students_export = students.drop(columns=['target_absence_rate', 'profil_absence', 'region_name'])

regions.to_csv(f"{OUTPUT_DIR}/region.csv", index=False, encoding='utf-8-sig')
schools.to_csv(f"{OUTPUT_DIR}/etablissement.csv", index=False, encoding='utf-8-sig')
classes.to_csv(f"{OUTPUT_DIR}/classe.csv", index=False, encoding='utf-8-sig')
students_export.to_csv(f"{OUTPUT_DIR}/student.csv", index=False, encoding='utf-8-sig')
teachers.to_csv(f"{OUTPUT_DIR}/teacher.csv", index=False, encoding='utf-8-sig')
teacher_assignments.to_csv(f"{OUTPUT_DIR}/teacher_subject_school.csv", index=False, encoding='utf-8-sig')
subjects.to_csv(f"{OUTPUT_DIR}/subject.csv", index=False, encoding='utf-8-sig')
time.to_csv(f"{OUTPUT_DIR}/time.csv", index=False, encoding='utf-8-sig')
grades.to_csv(f"{OUTPUT_DIR}/grades.csv", index=False, encoding='utf-8-sig')
attendance.to_csv(f"{OUTPUT_DIR}/attendance.csv", index=False, encoding='utf-8-sig')
student_metrics.to_csv(f"{OUTPUT_DIR}/student_metrics.csv", index=False, encoding='utf-8-sig')

print("\n" + "="*80)
print("DATASET AVEC VRAIE DIVERSITÉ RÉGIONALE")
print("="*80)

print(f"\nVUE GLOBALE")
print(f"   - Total élèves: {len(students):,}")
print(f"   - Total établissements: {len(schools)}")
print(f"   - Total classes: {len(classes)}")

print(f"\nCOMPARAISON RÉGIONALE DÉTAILLÉE")
print("-" * 80)

for _, region in regions.iterrows():
    region_name = region["region_name"]
    region_id = region["region_id"]

    region_students = students[students["region_name"] == region_name]
    region_schools = schools[schools["region_id"] == region_id]

    region_classes = classes[classes["school_id"].isin(region_schools["school_id"])]

    region_student_ids = region_students["student_id"]
    region_attendance = attendance[attendance["student_id"].isin(region_student_ids)]
    region_grades = grades[grades["student_id"].isin(region_student_ids)]
    region_metrics = student_metrics[student_metrics["student_id"].isin(region_student_ids)]
    
    absence_rate = (region_attendance['status'].str.contains('Absent').sum() / len(region_attendance)) * 100 if len(region_attendance) > 0 else 0
    avg_score = region_grades["score"].mean() if len(region_grades) > 0 else 0
    success_rate = (region_grades['status'] == 'Validé').sum() / len(region_grades) * 100 if len(region_grades) > 0 else 0
    
    print(f"\n{region_name}")
    print(f"   - Établissements: {len(region_schools)}")
    print(f"   - Classes: {len(region_classes)}")
    print(f"   - Élèves: {len(region_students):,}")
    print(f"   - Taux d'absentéisme: {absence_rate:.2f}%")
    print(f"   - Note moyenne: {avg_score:.2f}/20")
    print(f"   - Taux de réussite: {success_rate:.1f}%")

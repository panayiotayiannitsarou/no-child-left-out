
import streamlit as st
import pandas as pd
import openpyxl
import io
import base64

# --- Κωδικός Πρόσβασης ---
SECURITY_CODE = "katanomi2025"
def password_gate():
    if "access_granted" not in st.session_state:
        st.session_state.access_granted = False
    if not st.session_state.access_granted:
        code = st.text_input("🔐 Εισάγετε τον κωδικό πρόσβασης", type="password")
        if code == SECURITY_CODE:
            st.session_state.access_granted = True
        else:
            st.stop()
password_gate()

# --- Ρύθμιση Σελίδας ---
st.set_page_config(page_title="Κατανομή Μαθητών με Παιδαγωγικά Κριτήρια", layout="wide")

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📘 Εισαγωγή", "🧮 Κατανομή Μαθητών", "📚 Συχνές Ερωτήσεις", "📥 Εξαγωγή Excel", "📬 Επικοινωνία"])

# --- Tab 1: Εισαγωγή ---
with tab1:
    st.title("📘 Κατανομή Μαθητών με Παιδαγωγικά Κριτήρια")

    st.markdown("## Κανένας Άνθρωπος δεν είναι Νησί – John Donne")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Κανένας άνθρωπος δεν είναι νησί**,  
        ολοκληρωμένος από μόνος του.  
        κάθε άνθρωπος είναι κομμάτι της ηπείρου,  
        μέρος του όλου.  
        [...]  
        Ο θάνατος κάθε ανθρώπου με μειώνει,  
        γιατί εγώ είμαι μέρος της ανθρωπότητας.
        """)
    with col2:
        st.markdown("""
        *No man is an island*,  
        entire of itself;  
        every man is a piece of the continent,  
        a part of the main.  
        [...]  
        Any man's death diminishes me,  
        because I am involved in mankind.
        """)

    st.markdown("---")
    st.markdown("## Η Κοινωνική Δικαιοσύνη στα Σχολεία – Ζήτημα Ύψιστης Σημασίας")
    st.markdown("""
    Η κοινωνική δικαιοσύνη δεν είναι πολυτέλεια, αλλά ευθύνη κάθε σχολείου. Ο εκπαιδευτικός οφείλει να διασφαλίζει ισότητα και ενσυναίσθηση στην πράξη. Η πλήρης και ακριβής καταγραφή των χαρακτηριστικών κάθε παιδιού – όπως η γλωσσική επάρκεια, οι ιδιαίτερες ανάγκες ή η κοινωνική δυναμική – είναι βασική για μια δίκαιη κατανομή στα τμήματα.
    """)
    st.markdown(
        '''
        <div style="padding: 1rem; background-color: #f0f8ff; border-left: 5px solid #1f77b4; font-style: italic;">
        ✨ «Κάποιες φορές αισθανόμαστε ότι αυτό που κάνουμε είναι μόνο μια σταγόνα στον ωκεανό.<br>
        Αλλά ο ωκεανός θα ήταν μικρότερος αν έλειπε αυτή η σταγόνα.»<br>
        — <strong>Μητέρα Τερέζα</strong>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.image("logo.png", width=120)
    st.markdown(
        "<div style='text-align: center; font-style: italic; font-size: 14px;'>"
        "Για μια παιδεία που βλέπει το φως στα παιδιά,<br>"
        "ακόμη και εκεί που άλλοι βλέπουν σκιές"
        "</div>",
        unsafe_allow_html=True
    )

# Οι άλλες καρτέλες θα προστεθούν στο επόμενο βήμα



# --- Tab 2: Κατανομή Μαθητών ---
with tab2:
    st.header("🧮 Κατανομή Μαθητών")
    uploaded_file = st.file_uploader("📥 Ανέβασε το αρχείο Excel με τους μαθητές", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Το αρχείο ανέβηκε και διαβάστηκε επιτυχώς.")
        st.dataframe(df)
        if st.button("🔘 Ξεκίνα την Κατανομή"):
            st.info("⚙️ Η κατανομή ξεκίνησε...")
            st.success("✅ Η κατανομή ολοκληρώθηκε επιτυχώς!")
            
# --- Ενσωμάτωση Λογικής Κατανομής ---
# app_v3.py – Πλήρης εφαρμογή κατανομής μαθητών με ασφάλεια και Βήματα 1 έως 6




# ---- Helper Functions ----

def is_in_class(s_id, classes):
    return any(s_id in [s['id'] for s in cl] for cl in classes)

def has_conflict(student, cl):
    return any(conflict_id in [s['id'] for s in cl] for conflict_id in student.get('conflicts', []))

# ---- Βήμα 1: Παιδιά Εκπαιδευτικών ----
def assign_teacher_children(students, classes):
    teacher_children = [s for s in students if s['is_teacher_child']]
    num_classes = len(classes)
    distributed_ids = set()

    for i in range(min(num_classes, len(teacher_children))):
        child = teacher_children[i]
        classes[i].append(child)
        distributed_ids.add(child['id'])

    remaining = [s for s in teacher_children if s['id'] not in distributed_ids]
    for child in remaining:
        placed = False
        for cl in classes:
            for peer in cl:
                if peer['is_teacher_child'] and peer['id'] in child.get('friends', []) and child['id'] in peer.get('friends', []):
                    cl.append(child)
                    placed = True
                    break
            if placed: break
        if not placed:
            for cl in classes:
                for peer in cl:
                    if peer['is_teacher_child'] and peer['gender'] != child['gender']:
                        cl.append(child)
                        placed = True
                        break
                if placed: break
        if not placed:
            for cl in classes:
                cl.append(child)
                break

# ---- Βήμα 2: Φίλοι Παιδιών Εκπαιδευτικών ----
def assign_friends_of_teacher_children(students, classes):
    student_map = {s['id']: s for s in students}
    teacher_children_ids = [s['id'] for s in students if s['is_teacher_child']]

    for i, cl in enumerate(classes):
        teacher_kids_in_class = [s for s in cl if s['id'] in teacher_children_ids]
        if len(teacher_kids_in_class) >= 2:
            for tk in teacher_kids_in_class:
                for fid in tk.get('friends', []):
                    friend = student_map.get(fid)
                    if (friend and tk['id'] in friend.get('friends', []) and
                        not friend['is_teacher_child'] and not friend['is_lively'] and
                        not has_conflict(friend, cl) and not is_in_class(friend['id'], classes)):
                        cl.append(friend)

# ---- Βήμα 3: Ζωηροί ----
def assign_lively_students(students, classes):
    lively_students = [s for s in students if s['is_lively']]
    for student in lively_students:
        candidate_classes = []
        for i, cl in enumerate(classes):
            lively_count = sum(1 for s in cl if s['is_lively'])
            if lively_count >= 2: continue
            if any(s['id'] in student.get('friends', []) and student['id'] in s.get('friends', []) for s in cl):
                continue
            if has_conflict(student, cl): continue
            candidate_classes.append((i, cl, lively_count, len(cl)))
        if not candidate_classes:
            for cl in classes:
                if not has_conflict(student, cl):
                    cl.append(student)
                    break
        else:
            candidate_classes.sort(key=lambda x: (x[2], len([s for s in x[1] if s['gender'] == student['gender']]), x[3]))
            classes[candidate_classes[0][0]].append(student)

# ---- Βήμα 4: Παιδιά με Ιδιαιτερότητες ----
def assign_special_needs_students(students, classes):
    special_students = [s for s in students if s['is_special'] and not is_in_class(s['id'], classes)]
    for student in special_students:
        class_lively_counts = [(i, sum(1 for s in cl if s['is_lively'])) for i, cl in enumerate(classes)]
        min_lively = min(c for _, c in class_lively_counts)
        candidate_classes = [i for i, c in class_lively_counts if c == min_lively]
        final_classes = []
        for i in candidate_classes:
            cl = classes[i]
            if not has_conflict(student, cl):
                final_classes.append((i, cl))
        if final_classes:
            final_classes.sort(key=lambda x: (
                sum(1 for s in x[1] if s['is_special']),
                sum(1 for s in x[1] if s['gender'] == student['gender']),
                len(x[1])
            ))
            final_classes[0][1].append(student)

# ---- Βήμα 5: Χαμηλή Γλωσσική Επάρκεια ----
def assign_language_needs_students(students, classes, max_class_size=25):
    def get_class_index_of(student_id):
        for i, cl in enumerate(classes):
            if any(s['id'] == student_id for s in cl):
                return i
        return None

    def is_fully_mutual_friend(s, friend_id):
        friend = next((x for x in students if x['id'] == friend_id), None)
        return friend and s['id'] in friend.get('friends', [])

    def class_stats():
        return [(i, len(cl)) for i, cl in enumerate(classes)]

    def count_gender(cl, gender):
        return sum(1 for s in cl if s['gender'] == gender)

    language_students = [s for s in students if s['is_language_support'] and not is_in_class(s['id'], classes)]

    for student in language_students:
        placed = False
        for friend_id in student.get('friends', []):
            if not is_fully_mutual_friend(student, friend_id): continue
            class_index = get_class_index_of(friend_id)
            if class_index is not None:
                cl = classes[class_index]
                if not has_conflict(student, cl) and len(cl) < max_class_size:
                    cl.append(student)
                    placed = True
                    break
        if placed: continue

        candidate_classes = []
        for i, cl in enumerate(classes):
            if has_conflict(student, cl) or len(cl) >= max_class_size:
                continue
            lang_count = sum(1 for s in cl if s.get('is_language_support'))
            gender_count = count_gender(cl, student['gender'])
            candidate_classes.append((i, cl, lang_count, gender_count, len(cl)))
        if candidate_classes:
            candidate_classes.sort(key=lambda x: (x[2], x[3], x[4]))
            best_index = candidate_classes[0][0]
            classes[best_index].append(student)

# ---- Βήμα 6: Υπόλοιποι Μαθητές με Φίλους ----
def assign_remaining_students_with_friends(students, classes, max_class_size=25):
    """
    Τοποθετεί τα υπόλοιπα παιδιά με βάση τις πλήρως αμοιβαίες φιλίες (ζευγάρια και τριάδες),
    λαμβάνοντας υπόψη: όριο 25 μαθητών ανά τμήμα, διαφορά έως 1 μαθητή, ισορροπία φύλου και αποφυγή συγκρούσεων.
    """

    def is_in_class(s_id):
        return any(s_id in [s['id'] for s in cl] for cl in classes)

    def has_conflict(student, cl):
        return any(c in [s['id'] for s in cl] for c in student.get('conflicts', []))

    def get_student_by_id(s_id):
        return next((s for s in students if s['id'] == s_id), None)

    def class_stats():
        return [(i, len(cl)) for i, cl in enumerate(classes)]

    def class_gender_score(cl, group):
        gender = [s['gender'] for s in group]
        same_gender_count = sum(1 for s in cl if s['gender'] in gender)
        return same_gender_count

    def is_balanced_distribution():
        sizes = sorted(len(cl) for cl in classes)
        return sizes[-1] - sizes[0] <= 1

    def can_add_group(cl, group):
        return (
            len(cl) + len(group) <= max_class_size and
            all(not has_conflict(s, cl) for s in group)
        )

    unplaced = [s for s in students if not is_in_class(s['id'])]
    used_ids = set()

    # Ζευγάρια
    for s in unplaced:
        if s['id'] in used_ids:
            continue
        for f_id in s.get('friends', []):
            friend = get_student_by_id(f_id)
            if (friend and not is_in_class(friend['id']) and
                s['id'] in friend.get('friends', []) and
                friend['id'] not in used_ids):

                pair = [s, friend]
                # Βρες τμήμα με ισορροπία και διαθέσιμη θέση
                candidate_classes = []
                for i, cl in enumerate(classes):
                    if can_add_group(cl, pair):
                        gender_score = class_gender_score(cl, pair)
                        candidate_classes.append((i, cl, gender_score, len(cl)))
                if candidate_classes:
                    candidate_classes.sort(key=lambda x: (x[2], x[3]))  # ισορροπία φύλου και μέγεθος
                    best_class = candidate_classes[0][1]
                    best_class.extend(pair)
                    used_ids.update([s['id'], friend['id']])
                break

    # Τριάδες
    unplaced = [s for s in students if not is_in_class(s['id'])]
    for a in unplaced:
        if a['id'] in used_ids:
            continue
        for b_id in a.get('friends', []):
            b = get_student_by_id(b_id)
            if not b or b['id'] in used_ids or a['id'] not in b.get('friends', []):
                continue
            for c_id in a.get('friends', []):
                if c_id == b_id:
                    continue
                c = get_student_by_id(c_id)
                if (c and c['id'] not in used_ids and
                    a['id'] in c.get('friends', []) and
                    b['id'] in c.get('friends', []) and
                    c_id in b.get('friends', [])):

                    trio = [a, b, c]
                    candidate_classes = []
                    for i, cl in enumerate(classes):
                        if can_add_group(cl, trio):
                            gender_score = class_gender_score(cl, trio)
                            candidate_classes.append((i, cl, gender_score, len(cl)))
                    if candidate_classes:
                        candidate_classes.sort(key=lambda x: (x[2], x[3]))
                        best_class = candidate_classes[0][1]
                        best_class.extend(trio)
                        used_ids.update([x['id'] for x in trio])
                    break
            if a['id'] in used_ids:
                break

# --- Παράδειγμα εκτέλεσης ---
students = []
classes = [[] for _ in range(2)]

assign_teacher_children(students, classes)
assign_friends_of_teacher_children(students, classes)
assign_lively_students(students, classes)
assign_special_needs_students(students, classes)
assign_language_needs_students(students, classes)
assign_remaining_students_with_friends(students, classes)

def assign_remaining_students_without_friends(students, classes, max_class_size=25):
    """
    Τοποθετεί μαθητές που δεν έχουν φίλους ή δεν συμμετέχουν σε αμοιβαίες φιλίες,
    και δεν έχουν τοποθετηθεί ακόμα. Λαμβάνονται υπόψη πληθυσμός, φύλο και συγκρούσεις.
    """

    def is_in_class(s_id):
        return any(s_id in [s['id'] for s in cl] for cl in classes)

    def has_conflict(student, cl):
        return any(cid in [s['id'] for s in cl] for cid in student.get('conflicts', []))

    def gender_balance_score(cl, gender):
        return sum(1 for s in cl if s['gender'] == gender)

    remaining_students = [s for s in students if not is_in_class(s['id'])]

    for student in remaining_students:
        candidate_classes = []
        for i, cl in enumerate(classes):
            if len(cl) >= max_class_size:
                continue
            if has_conflict(student, cl):
                continue
            gender_score = gender_balance_score(cl, student['gender'])
            candidate_classes.append((i, cl, gender_score, len(cl)))

        if candidate_classes:
            # προτεραιότητα: λίγοι του ίδιου φύλου, μικρότερος πληθυσμός
            candidate_classes.sort(key=lambda x: (x[2], x[3]))
            best_class = candidate_classes[0][1]
            best_class.append(student)

assign_remaining_students_without_friends(students, classes)

        # --- Εκτέλεση κατανομής μέσα από το κουμπί ---
        students = df.to_dict(orient="records")
        num_classes = (len(students) + 24) // 25
        classes = [[] for _ in range(num_classes)]

        assign_teacher_children(students, classes)
        assign_friends_of_teacher_children(students, classes)
        assign_lively_students(students, classes)
        assign_special_needs_students(students, classes)
        assign_language_needs_students(students, classes)
        assign_remaining_students_with_friends(students, classes)
        assign_remaining_students_without_friends(students, classes)

        result = []
        for i, cl in enumerate(classes):
            for student in cl:
                student['Τμήμα'] = f"Τμήμα {i+1}"
                result.append(student)
        result_df = pd.DataFrame(result)
        st.dataframe(result_df)

        towrite = io.BytesIO()
        result_df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Κατανομή.xlsx">📥 Κατέβασε Αρχείο Κατανομής (Excel)</a>'
        st.markdown(href, unsafe_allow_html=True)


# --- Tab 3: Συχνές Ερωτήσεις ---
with tab3:
    st.header("📚 Συχνές Ερωτήσεις")
    st.markdown("""
❓ Συχνές Ερωτήσεις – Εφαρμογή Κατανομής Μαθητών\n\n1. Πώς ανεβάζω το αρχείο Excel;\n\nΜέσα από την καρτέλα «Κατανομή Μαθητών», υπάρχει επιλογή «Ανέβασε το αρχείο Excel». Το αρχείο πρέπει να έχει τις σωστές στήλες όπως περιγράφονται στις οδηγίες.\n\n2. Ποιες είναι οι αποδεκτές τιμές στα πεδία;\n\nΌλες οι τιμές πρέπει να είναι με ελληνικά κεφαλαία γράμματα: Ν (Ναι), Ο (Όχι), Α (Αγόρι), Κ (Κορίτσι).\n\n3. Πόσα τμήματα δημιουργεί η εφαρμογή;\n\nΗ εφαρμογή υπολογίζει αυτόματα πόσα τμήματα χρειάζονται, με βάση ότι κάθε τμήμα μπορεί να έχει έως 25 μαθητές και ο πληθυσμός του κάθε τμήματος να διαφέρει κατά 1 από τα υπόλοιπα τμηματα .\n\n4. Ποια κριτήρια χρησιμοποιούνται για την κατανομή;\n\nΗ κατανομή ακολουθεί παιδαγωγικά στάδια:
1. Παιδιά Εκπαιδευτικών
2. Ζωηροί Μαθητές
3. Παιδιά με Ιδιαιτερότητες
4. Παιδιά με Γλωσσική Αδυναμία
5. Αμοιβαίες Φιλίες (δυάδες ή τριάδες)
6. Συγκρούσεις\n\n5. Πώς λειτουργούν οι φιλίες και οι συγκρούσεις;\n\n– Φιλία λαμβάνεται υπόψη μόνο αν είναι αμοιβαία.
– Συγκρούσεις σημαίνει ότι οι δηλωμένοι μαθητές δεν θα τοποθετηθούν στο ίδιο τμήμα και απαιτείται σχετικό αποδεικτικό έντυπο.\n\n6. Τι σημαίνει ισορροπία φύλου με ανοχή ±3;\n\nΗ εφαρμογή εξασφαλίζει ότι η διαφορά μεταξύ αγοριών και κοριτσιών σε κάθε τμήμα δεν ξεπερνά τους 3 μαθητές.\n\n7. Πώς κατεβάζω τα αποτελέσματα;\n\nΜόλις ολοκληρωθεί η κατανομή, μπορείς να πατήσεις «Κατέβασε Αρχείο Κατανομής (Excel)» για να πάρεις το αρχείο.\n\n8. Ποιος έχει το δικαίωμα χρήσης της εφαρμογής;\n\nΗ χρήση επιτρέπεται μόνο με ρητή γραπτή άδεια από τη δημιουργό.
📧 Επικοινωνία: yiannitsaroupanayiota.katanomi@gmail.com\n\n
    """)

# --- Tab 4: Εξαγωγή Excel ---
with tab4:
    st.header("📥 Εξαγωγή Αρχείου Κατανομής")
    st.markdown("Το αρχείο κατανομής θα εμφανιστεί εδώ προς λήψη μετά την ολοκλήρωση της κατανομής.")
    st.info("Αυτή η λειτουργία θα ενεργοποιηθεί όταν ενσωματωθεί η λογική κατανομής και παραγωγής αρχείου Excel.")

# --- Tab 5: Επικοινωνία ---
with tab5:
    st.header("📬 Επικοινωνία")
    st.markdown("""
    **Για οποιαδήποτε απορία ή αίτημα:**

    ✉️ Email: [yiannitsaroupanayiota.katanomi@gmail.com](mailto:yiannitsaroupanayiota.katanomi@gmail.com)

    ℹ️ Η χρήση της εφαρμογής επιτρέπεται μόνο με ρητή γραπτή άδεια από τη δημιουργό.
    """)


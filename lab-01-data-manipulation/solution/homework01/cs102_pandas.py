import pandas as pd
import re
from typing import Tuple


# Задача 1
def filter_fsuir_students(data: pd.DataFrame) -> Tuple[int, int, pd.DataFrame]:
    """
    Создает подвыборку студентов факультета систем управления и робототехники (ФСУиР).
    Возвращает количество таких студентов, количество уникальных групп и отфильтрованный датасет.
    """
    filtered_data = data[data['факультет'] == 'факультет систем управления и робототехники']
    return filtered_data.shape[0], filtered_data['группа'].nunique(), filtered_data


# Задача 2
def find_homonymous_students(df: pd.DataFrame) -> Tuple[bool, int, pd.Series, str]:
    """
    Проверяет наличие однофамильцев на ФСУиР, их количество, распределение по курсам
    и определяет группу с наибольшим числом однофамильцев.
    Возвращает:
     - логическое значение (наличие однофамильцев)
     - общее количество однофамильцев
     - серию с числом однофамильцев по курсам
     - группу с максимальным числом однофамильцев
    """
    surname_counts = df["surname"].value_counts()
    homonymous_surnames = surname_counts[surname_counts > 1].index
    total_homonymous = df["surname"].isin(homonymous_surnames).sum()

    per_course = {}
    for course in df["курс"].unique():
        course_df = df[df["курс"] == course]
        course_surname_counts = course_df["surname"].value_counts()
        homonymous_course_surnames = course_surname_counts[course_surname_counts > 1].index
        per_course[course] = course_df["surname"].isin(homonymous_course_surnames).sum()
    hom_per_course = pd.Series(per_course).sort_index()

    group_counts = {}
    for group in df["группа"].unique():
        group_df = df[df["группа"] == group]
        group_surname_counts = group_df["surname"].value_counts()
        homonymous_group_surnames = group_surname_counts[group_surname_counts > 1].index
        group_counts[group] = group_df["surname"].isin(homonymous_group_surnames).sum()
    return total_homonymous > 0, total_homonymous, hom_per_course, max(group_counts, key=group_counts.get)
    

# Задача 3
def gender_identification(patronym: str) -> str:
    """
    Определяет пол по отчеству. Возвращает пол: female/male/unknown.
    """
    male_endings = ("ович", "евич", "ич")
    female_endings = ("овна", "евна", "ична", "инична")
    if patronym.endswith(male_endings):
        return "male"
    elif patronym.endswith(female_endings):
        return "female"
    else:
        return "unknown"


def analyze_patronyms(df: pd.DataFrame) -> Tuple[int, pd.Series]:
    """
    Определяет количество студентов без отчества и распределение студентов по полу на основе отчества.
    Возвращает:
     - количество студентов без отчества
     - серию с распределением студентов по полу 
    """
    no_patronyms = df[df['фио'].str.split().str.len() == 2]
    with_patronyms = df[df['фио'].str.split().str.len() == 3]
    with_patronyms['patronym'] = with_patronyms["фио"].str.split().str[2]
    with_patronyms['gender'] = with_patronyms['patronym'].apply(gender_identification)
    gender_count = with_patronyms["gender"].value_counts()
    return no_patronyms.shape[0], gender_count


# Задача 4
def faculty_statistics(data: pd.DataFrame) -> Tuple[pd.DataFrame, Tuple[str, int], Tuple[str, int]]:
    """
    Подсчитывает количество студентов на каждом факультете,
    а также определяет факультеты с максимальным и минимальным числом студентов.
    """
    on_faculty = data['факультет'].value_counts().reset_index(name="количество студентов")
    max_students_faculty = (on_faculty.iloc[0]['факультет'], int(on_faculty.iloc[0]['количество студентов']))
    min_students_faculty = (on_faculty.iloc[-1]['факультет'], int(on_faculty.iloc[-1]['количество студентов']))
    return on_faculty, max_students_faculty, min_students_faculty

# Задача 5
def course_statistics(data: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    Вычисляет среднее и медианное число студентов на каждом курсе.
    Возвращает две серии с результатами: сначала средние, потом медиана.
    """
    students_by_course_faculty = data.groupby(['факультет', 'курс']).size().reset_index(name="количество студентов")
    average = students_by_course_faculty.groupby('курс')['количество студентов'].mean()
    median = students_by_course_faculty.groupby('курс')['количество студентов'].median()
    return average, median


# Задача 6
def most_popular_name(data: pd.DataFrame) -> Tuple[str, str, str, str, float]:
    """
    Определяет самое популярное имя, группу с наибольшим количеством студентов с этим именем,
    факультет, курс и долю таких студентов в общем числе.
    Возвращает результат в следующем порядке:
     1. самое частое имя
     2. группа
     3. факультет
     4. доля
    """
    data['name'] = data['фио'].str.split().str[1]
    name_count = data['name'].value_counts()
    most_popular_name = name_count.idxmax()
    popular_name_data = data[data['name'] == most_popular_name]
    max_name_freq_group = popular_name_data.groupby('группа').size().idxmax()
    faculty = data[data['группа'] == max_name_freq_group].iloc[0]['факультет']
    course = data[data['группа'] == max_name_freq_group].iloc[0]['курс']
    fraction = float(round(name_count.iloc[0] / data.shape[0], 2))
    return most_popular_name, max_name_freq_group, faculty, course, fraction


# Задача 7
def find_students_with_name_starting_P(data: pd.DataFrame) -> pd.DataFrame:
    """
    Находит студентов, чье имя встречается ровно один раз и начинается на "П". Выводит их ФИО, факультет и курс.
    """
    data['name'] = data['фио'].str.split().str[1]
    data_p_name = data[data['name'].str.startswith('П')]
    p_name_count = data_p_name['name'].value_counts()
    p_name_count_one = p_name_count[p_name_count == 1].index
    data_p_one = data[data['name'].isin(p_name_count_one)]
    return data_p_one[['фио', 'факультет', 'курс'].copy()]



# Задача 8
def highest_avg_grade_faculty(data: pd.DataFrame) -> Tuple[str, str, int]:
    """
    Находит факультет, на котором средний балл студентов третьего курса самый высокий.
    Определяет пол, средний балл котого выше.
    Сначала возвращает факультет, затем пол, затем балл.
    """
    third_course = data[data['курс'] == '3-й']
    third_course['patronym'] = None
    name_parts = third_course['фио'].str.split()
    third_course.loc[name_parts.str.len() >= 3, 'patronym'] = name_parts[name_parts.str.len() >= 3].str[2]
    highest_faculty = third_course.groupby('факультет')['средний_балл'].mean().idxmax()
    highest_faculty_students = third_course[third_course['факультет'] == highest_faculty]
    highest_faculty_students['gender'] = highest_faculty_students['patronym'].apply(gender_identification)
    gender_average = highest_faculty_students.groupby('gender')['средний_балл'].mean()
    return highest_faculty, gender_average.idxmax(), int(round(gender_average.max()))

# Задача 9
def find_consecutive_students(data: pd.DataFrame) -> pd.DataFrame:
    """
    Находит первых 5 студентов, которым номера были присвоены подряд.
    Выводит их ФИО, факультет, курс и номер группы.
    """
    sorted_data = data.sort_values('ису')
    sorted_data['sequence_id'] = (sorted_data['ису'].diff() != 1).cumsum()
    sequence_sizes = sorted_data.groupby('sequence_id').size()
    five_students = sequence_sizes[sequence_sizes >= 5].index[0]
    return sorted_data[sorted_data['sequence_id'] == five_students].head(5)

if __name__ == "__main__":
    data = pd.read_csv("isu_fake_data.csv")
    data["surname"] = data['фио'].str.split().str[0]
    data["name"] = data['фио'].str.split().str[1]
    data["patronim"] = data['фио'].str.split().str[2]
    
    # Задача 1
    num_students, num_groups, fsuir = filter_fsuir_students(data)
    print(f"Студентов на ФСУиР: {num_students}, Групп: {num_groups}")
    
    # Задача 2
    has_homonyms, total_homonyms, homonyms_per_course, max_homonym_group = find_homonymous_students(fsuir)
    print(f"Есть однофамильцы: {has_homonyms}, Всего: {total_homonyms}, Группа с максимумом: {max_homonym_group}")
    print(f"На каждом курсе: {homonyms_per_course}")
    
    # Задача 3
    students_without_patronym, gender_counts = analyze_patronyms(fsuir)
    print(f"Студентов без отчества: {students_without_patronym}")
    print("Распределение по полу:", gender_counts)
    
    # Задача 4
    faculty_counts, max_faculty, min_faculty = faculty_statistics(data)
    print(f"Факультет с наибольшим числом студентов: {max_faculty}")
    print(f"Факультет с наименьшим числом студентов: {min_faculty}")
    
    # Задача 5
    mean_students, median_students = course_statistics(data)
    print("Среднее число студентов на курсах:", mean_students)
    print("Медианное число студентов на курсах:", median_students)
    
    # Задача 6
    popular_name, name_group, faculty, course, name_ratio = most_popular_name(data)
    print(f"Самое популярное имя: {popular_name}, Группа: {name_group}, Факультет: {faculty}, Курс: {course}")
    print(f"Доля студентов с этим именем: {name_ratio}")
    
    # Задача 7
    result_7 = find_students_with_name_starting_P(data)
    print("Студенты с именем, начинающимся на П и встречающимся ровно один раз:")
    print(result_7)
    
    # Задача 8
    fac, best_gender, best_grade = highest_avg_grade_faculty(data)
    print(f"Факультет с высоким средним баллом 3-го курса: {fac}")
    print(f"Пол с наивысшим средним баллом: {best_gender}, Средний балл: {best_grade}")
    
    # Задача 9
    result_9 = find_consecutive_students(data)
    print("Первые 5 студентов с подряд идущими табельными номерами:")
    print(result_9)

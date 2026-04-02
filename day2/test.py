# =============================
# HRM SYSTEM - DAY 2 (OOP + ADVANCED)
# =============================

from typing import List

# ========== DECORATOR ==========
# Decorator dùng để log khi gọi hàm
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}...")  # In ra tên hàm đang chạy
        return func(*args, **kwargs)  # Gọi lại hàm gốc
    return wrapper

# ========== BASE CLASS ==========
# Lớp cơ bản Employee
class Employee:
    def __init__(self, name: str, salary: float):
        self.name = name          # Tên nhân viên
        self.salary = salary      # Lương cơ bản

    def get_salary(self) -> float:
        return self.salary        # Trả về lương

    def __str__(self):
        return f"Employee: {self.name} | Salary: {self.get_salary()}"  # Hiển thị thông tin

# ========== INHERITANCE ==========
# Manager kế thừa từ Employee
class Manager(Employee):
    def __init__(self, name: str, salary: float, bonus: float):
        super().__init__(name, salary)  # Gọi constructor cha
        self.bonus = bonus              # Thưởng thêm

    def get_salary(self) -> float:
        return self.salary + self.bonus  # Lương = lương cơ bản + thưởng

# Intern kế thừa Employee
class Intern(Employee):
    def get_salary(self) -> float:
        return self.salary * 0.5  # Intern chỉ nhận 50% lương

# ========== CONTEXT MANAGER ==========
# Dùng để quản lý file (tự động mở/đóng file)
class FileManager:
    def __init__(self, filename: str):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "w", encoding="utf-8")  # Mở file
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()  # Đóng file khi xong

# ========== HRM SYSTEM ==========
# Lớp quản lý toàn bộ nhân viên
class HRM:
    def __init__(self):
        self.employees: List[Employee] = []  # Danh sách nhân viên

    def add_employee(self, emp: Employee):
        self.employees.append(emp)  # Thêm nhân viên vào list

    def show_all(self):
        if not self.employees:
            print("No employees.")
        for e in self.employees:
            print(e)  # In từng nhân viên

    @log_action
    def total_salary(self):
        # Tính tổng lương tất cả nhân viên
        return sum(e.get_salary() for e in self.employees)

    def find_by_name(self, name: str):
        # Tìm nhân viên theo tên (không phân biệt hoa thường)
        return [e for e in self.employees if e.name.lower() == name.lower()]

    def delete_by_name(self, name: str):
        # Xóa nhân viên theo tên
        self.employees = [e for e in self.employees if e.name.lower() != name.lower()]

    # ========== GENERATOR ==========
    def employee_generator(self):
        # Duyệt từng nhân viên bằng yield (tiết kiệm bộ nhớ)
        for e in self.employees:
            yield e

    # ========== SAVE TO FILE ==========
    def save_to_file(self, filename="employees.txt"):
        # Lưu danh sách nhân viên ra file
        with FileManager(filename) as f:
            for e in self.employees:
                f.write(str(e) + "\n")

# ========== CONSOLE APP ==========
# Menu hiển thị chức năng
def menu():
    print("""
==== HRM SYSTEM ====
1. Add Employee
2. Show All
3. Total Salary
4. Find Employee
5. Delete Employee
6. Save to File
0. Exit
""")

# Hàm main chạy chương trình
def main():
    hrm = HRM()

    while True:
        menu()
        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            salary = float(input("Salary: "))
            emp_type = input("Type (employee/manager/intern): ").lower()

            if emp_type == "manager":
                bonus = float(input("Bonus: "))
                emp = Manager(name, salary, bonus)
            elif emp_type == "intern":
                emp = Intern(name, salary)
            else:
                emp = Employee(name, salary)

            hrm.add_employee(emp)

        elif choice == "2":
            hrm.show_all()

        elif choice == "3":
            print("Total salary:", hrm.total_salary())

        elif choice == "4":
            name = input("Enter name: ")
            result = hrm.find_by_name(name)
            for e in result:
                print(e)

        elif choice == "5":
            name = input("Enter name to delete: ")
            hrm.delete_by_name(name)

        elif choice == "6":
            hrm.save_to_file()
            print("Saved to file!")

        elif choice == "0":
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()

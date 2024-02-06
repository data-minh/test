import urllib.request
import xml.etree.ElementTree as ET
import json


class Employee():
    def __init__(self, id, name, salary_base, working_days, department, working_performance, bonus, late_comming_days):
        self.id = id
        self.name = name
        self.salary_base = salary_base
        self.working_days = working_days
        self.department = department
        self.working_performance = working_performance
        self.bonus = bonus
        self.late_comming_days = late_comming_days

    def load_tax_data(self):
        link_taxs = "https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien%2FPYB101x_1.1%2FASM_Resources%2Ftax.xml?alt=media&token=f7a6f73d-9e6d-4807-bb14-efc6875442c7"
        open_taxs = urllib.request.urlopen(link_taxs).read()
        open_taxs_stuff = ET.fromstring(open_taxs)

        tax_data = []

        for i in open_taxs_stuff.findall('tax'):
            min_element = i.find('min')
            max_element = i.find('max')
            value_element = i.find('value')

            if min_element is not None and max_element is not None and value_element is not None:
                min_value = float(min_element.text)
                max_value = float(max_element.text)
                pham_tram_tax = float(value_element.text)

                tax_info = {
                    'min': min_value,
                    'max': max_value,
                    'value': pham_tram_tax
                }

                tax_data.append(tax_info)
        return tax_data

    def load_late_coming_penalty(self):
        link_phat = "https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien%2FPYB101x_1.1%2FASM_Resources%2Flate_coming.json?alt=media&token=55246ee9-44fa-4642-aca2-dde101d705de"
        open_phat = urllib.request.urlopen(link_phat).read()
        late_coming_info = json.loads(open_phat)
        return late_coming_info

    def calculate_salary(self, bonus_department):
        # Tính thu nhập chưa thưởng và thưởng bộ phận
        base_income = (self.salary_base * self.working_days) * self.working_performance
        department_bonus = bonus_department.bonus_salary
        total_bonus = float(str(department_bonus).replace(',', '')) + float(str(self.bonus).replace(',', ''))

        # Tính tiền phạt đi muộn
        late_coming_penalty = 0
        for penalty_info in self.load_late_coming_penalty():
            if self.late_comming_days >= penalty_info['min'] and self.late_comming_days <= penalty_info['max']:
                late_coming_penalty = self.late_comming_days * penalty_info['value']
                break

        # Tính thu nhập chưa thuế
        total_income_before_tax = base_income + total_bonus - late_coming_penalty

        # Trừ thuế thu nhập cá nhân
        tax_rate = 0
        for tax_info in self.load_tax_data():
            if total_income_before_tax >= tax_info['min'] and total_income_before_tax <= tax_info['max']:
                tax_rate = tax_info['value']
                break

        tax = (total_income_before_tax * tax_rate) / 100
        total_income = total_income_before_tax - tax

        return total_income


class Manager(Employee):
    def __init__(self, id, name, salary_base, working_days, department, working_performance, bonus, late_comming_days):
        super().__init__(id, name, salary_base, working_days, department, working_performance, bonus, late_comming_days)

    # Thưởng bộ phận của quản lý sẽ nhận thêm 10% so với nhân viên bình thường
    def calculate_salary(self, bonus_department):
        # Tính thu nhập chưa thưởng và thưởng bộ phận
        base_income = (self.salary_base * self.working_days) * self.working_performance
        department_bonus = bonus_department.bonus_salary
        total_bonus = department_bonus + self.bonus + department_bonus * 0.1  # Cộng thêm 10% so với nhận viên bình thường

        # Tính tiền phạt đi muộn
        late_coming_penalty = 0
        for penalty_info in self.load_late_coming_penalty():
            if self.late_comming_days >= penalty_info['min'] and self.late_comming_days <= penalty_info['max']:
                late_coming_penalty = self.late_comming_days * penalty_info['value']
                break

        # Tính thu nhập chưa thuế
        total_income_before_tax = base_income + total_bonus - late_coming_penalty

        # Trừ thuế thu nhập cá nhân
        tax_rate = 0
        for tax_info in self.load_tax_data():
            if total_income_before_tax >= tax_info['min'] and total_income_before_tax <= tax_info['max']:
                tax_rate = tax_info['value']
                break

        tax = (total_income_before_tax * tax_rate) / 100
        total_income = total_income_before_tax - tax

        return total_income


class Department():
    def __init__(self, department, bonus_salary):
        self.department = department
        self.bonus_salary = bonus_salary


print('_' * 50)


def hien_thi_danh_sach_nhan_vien():
    # Tên tệp JSON
    link_file_persons = 'data_persons.json'
    # Đọc tệp JSON
    with open(link_file_persons, 'r', encoding='utf-8') as file:
        data_person = json.load(file)

    # Truy cập vào thông tin của danh sách
    for person in data_person:
        # In các thông tin của nhân viên được lưu
        print("Mã số:", person["Mã số"])
        print("Mã bộ phận:", person["Mã bộ phận"])
        print("Chức vụ:", person["Chức vụ"])
        print("Họ tên:", person["Họ tên"])
        print("Hệ số lương:", person["Hệ số lương"])
        print("Số ngày làm việc:", person["Số ngày làm việc"])
        print("Hệ số hiệu quả:", person["Hệ số hiệu quả"])
        print("Thưởng:", person["Thưởng"])
        print("Số ngày đi muộn:", person["Số ngày đi muộn"])
        print("-" * 50)


def hien_thi_danh_sach_bo_phan():
    # Tên tệp JSN
    link_file_department = 'data_departments.json'
    # Đọc tệp JSON
    with open(link_file_department, 'r', encoding='utf-8') as file:
        data_department = json.load(file)

    # Truy cập thông tin của danh sách
    for department in data_department:
        # In mã các bộ phận ứng với những khoản tiền thưởng đi cùng
        print("Mã bộ phận: ", department['Mã bộ phận'])
        print("Thưởng bộ phận: ", department['Thưởng bộ phận'])
        print('_' * 50)


def them_nhan_vien_moi():
    files_data_persons = "data_persons.json"
    try:
        with open(files_data_persons, 'r', encoding='utf-8') as json_file_data_persons:
            lst_persons = json.load(json_file_data_persons)
    except:
        lst_persons = []
    print(lst_persons)
    # Lập danh sách những ID nhân viên hiện tại đang có trong file được lưu
    lst_id = []
    for id in lst_persons:
        lst_id.append(id['Mã số'])

    # Lập danh sách những phòng ban hiện tại đang có trong file được lưu
    files_data_department = "data_departments.json"
    try:
        with open(files_data_department, "r", encoding="utf-8") as json_file_data_department:
            lst_departments = json.load(json_file_data_department)
    except:
        lst_departments = []

    lst_code_department = []
    for code_department in lst_departments:
        lst_code_department.append(code_department['Mã bộ phận'])

    print("Thêm nhân viên mới...")
    # Tạo một dict() là nhân viên mới muốn thêm vào
    datas = dict()
    while True:
        datas['Mã số'] = str(input('Nhập mã số nhận viên: '))
        if datas['Mã số'] == '':
            print("Bạn không được bỏ trống thông tin này")
        elif datas['Mã số'] in lst_id:
            print("Mã nhân viên đã tồn tại")
        else:
            break
    while True:
        datas['Mã bộ phận'] = str(input('Nhập mã bộ phận: '))
        if datas['Mã bộ phận'] == '':
            print("Bạn không được bỏ trống thông tin này")
        elif datas['Mã bộ phận'] not in lst_code_department:
            print("Mã bộ phận chưa tồn tại, tạo mới...")
            # Thêm một dict mới để thêm vào list department hiện tại
            department = dict()
            department['Mã bộ phận'] = datas['Mã bộ phận']
            department['Thưởng bộ phận'] = '{:,.0f}'.format(float(input('Nhập thưởng bộ phận: ')))
            # Chèn dict mới vào list department hiện tại đang có
            lst_departments.append(department)

            # Sau khi hoàn thành thì thêm thông tin bộ phận mới vào file json
            with open(files_data_department, "w", encoding="utf-8") as json_file_data_department:
                json.dump(lst_departments, json_file_data_department, ensure_ascii=False, indent=4)

            print("Đã tạo bộ phận mới ...")
            # Hoàn thành thêm một department mới nếu khi nhập phát hiện ra phòng ban đấy chưa tồn tại
            break

        else:
            break
    while True:
        datas['Chức vụ'] = str(input('Nhập chức vụ của nhân viên: '))
        if datas['Chức vụ'] == '':
            print("Bạn không được bỏ trống thông tin này")
        else:
            break
    while True:
        datas['Họ tên'] = str(input('Nhập họ và tên: '))
        if datas['Họ tên'] == '':
            print("Bạn không được bỏ trống thông tin này")
        else:
            break

    while True:
        try:
            datas['Hệ số lương'] = '{:,.0f}'.format(float(input(f'Nhập hệ số lương cơ bản: ')))
            if float(datas['Hệ số lương'].replace(',', '')) < 0:
                print("Bạn phải nhập một số không âm")
            else:
                break
        except ValueError:
            print("Bạn không được bỏ trống thông tin này")

    while True:
        try:
            datas['Số ngày làm việc'] = float(input('Nhập số ngày làm việc: '))
            if datas['Số ngày làm việc'] < 0:
                print("Bạn phải nhập số không âm")
            else:
                break
        except ValueError:
            print("Bạn không được bỏ trống thông tin này")

    while True:
        try:
            datas['Hệ số hiệu quả'] = float(input('Nhập hệ số hiệu quả: '))
            if datas['Hệ số hiệu quả'] < 0:
                print("Bạn phải nhập số không âm")
            else:
                break
        except ValueError:
            print("Bạn không được bỏ trống thông tin này")

    while True:
        try:
            datas['Thưởng'] = '{:,.0f}'.format(float(input('Nhập thưởng: ')))
            if float(datas['Thưởng'].replace(',', '')) < 0:
                print("Bạn phải nhập số không ân")
            else:
                break
        except ValueError:
            print("Bạn không được bỏ trống thông tin này")
    while True:
        try:
            datas['Số ngày đi muộn'] = float(input('Nhập số ngày đi muộn: '))
            if datas['Số ngày đi muộn'] < 0:
                print("Bạn phải nhập số không âm")
            else:
                break
        except ValueError:
            print("Bạn không được bỏ trống thông tin này")

    # Thêm dict của nhân viên mới nhập thông tin vào list thông tin của nhân viên
    lst_persons.append(datas)
    # Viết dữ liệu vào file, sử dụng json.dump()
    with open(files_data_persons, "w", encoding="utf-8") as json_file_datas:
        json.dump(lst_persons, json_file_datas, ensure_ascii=False, indent=4)

    print("Đã thêm nhân viên mới")


def xoa_nhan_vien_theo_id():
    files_data_persons = "data_persons.json"
    try:
        with open(files_data_persons, 'r', encoding='utf-8') as json_file_data_persons:
            lst_persons = json.load(json_file_data_persons)
    except:
        lst_persons = []
    # Lập danh sách những ID nhân viên hiện tại đang có trong file được lưu
    lst_id = []
    for id in lst_persons:
        lst_id.append(id['Mã số'])

    while True:
        print("Nếu không muốn tiếp tục thực hiện chương trình chọn 0")
        chon = input("Nhập mã nhân viên bạn muốn xóa: ")
        if chon == "0":
            print("Đã thoát")
            break
        else:
            if chon in lst_id:
                save_chon = 0
                for i in range(len(lst_id)):
                    if chon == lst_id[i]:
                        save_chon = i
                del lst_persons[save_chon]
            # Lưu lại kết quả sau khi xóa
            with open(files_data_persons, "w", encoding="utf-8") as json_file_datas:
                json.dump(lst_persons, json_file_datas, ensure_ascii=False, indent=4)

            print("Đã xóa nhân viên theo ID")
            break


def xoa_bo_phan_theo_id():
    # Lập danh sách những phòng ban hiện tại đang có trong file được lưu
    files_data_department = "data_departments.json"
    try:
        with open(files_data_department, "r", encoding="utf-8") as json_file_data_department:
            lst_departments = json.load(json_file_data_department)
    except:
        lst_departments = []

    lst_code_department = []
    for code_department in lst_departments:
        lst_code_department.append(code_department['Mã bộ phận'])

    # Lập danh sách những phòng ban hiện tại đang có nhân viên
    files_data_persons = "data_persons.json"
    try:
        with open(files_data_persons, 'r', encoding='utf-8') as json_file_data_persons:
            lst_persons = json.load(json_file_data_persons)
    except:
        lst_persons = []

    lst_code_department_current_have_person = []
    for code_department_current in lst_persons:
        lst_code_department_current_have_person.append(code_department_current['Mã bộ phận'])

    # Dùng vòng lặp để xóa department mong muốn
    while True:
        print("Nếu không muốn tiếp tục thực hiện chương trình chọn 0")
        chon = input("Nhập mã departments bạn muốn xóa: ")
        if chon == "0":
            print("Đã thoát")
            break
        elif chon not in lst_code_department:
            print("Department bạn muốn xóa hiện tại không có trong danh sách")
            break
        else:
            if chon in lst_code_department_current_have_person:
                print("Bạn không thể xóa bộ phận đang có nhân viên")
                break
            else:
                chon_code_department_save = 0
                for i in range(len(lst_code_department)):
                    if chon == lst_code_department[i]:
                        chon_code_department_save = i
                del lst_departments[chon_code_department_save]
            # Lưu lại kết quả sau khi thực hiện xóa
            with open(files_data_department, "w", encoding="utf-8") as json_file_data_department:
                json.dump(lst_departments, json_file_data_department, ensure_ascii=False, indent=4)

            print("Đã xóa nhân viên theo ID")
            break


def hien_thi_bang_luong():
    # Mở file data_persons và lấy dữ liệu
    files_data_persons = "data_persons.json"
    try:
        with open(files_data_persons, 'r', encoding='utf-8') as json_file_data_persons:
            lst_persons = json.load(json_file_data_persons)
    except:
        lst_persons = []

    # Mở file data_department và lấy dữ liệu
    files_data_department = "data_departments.json"
    try:
        with open(files_data_department, "r", encoding="utf-8") as json_file_data_department:
            lst_departments = json.load(json_file_data_department)
    except:
        lst_departments = []

    # Dùng vòng lặp để xét tất cả các nhân viên hiện tại
    for person in lst_persons:
        if person['Chức vụ'] == "Nhân viên":
            # Do hệ số lương đang ở dạng str chính vì vậy cần chuyển qua float để tính toán
            he_so_luong = float(str(person['Hệ số lương']).replace(',', ''))
            employee = Employee(person['Mã số'], person['Họ tên'], he_so_luong, person['Số ngày làm việc'],
                                person['Mã bộ phận'], person['Hệ số hiệu quả'], person['Thưởng'],
                                person['Số ngày đi muộn'])

            for department in lst_departments:
                if department['Mã bộ phận'] == person['Mã bộ phận']:
                    bonus_salary = department['Thưởng bộ phận']

        elif person['Chức vụ'] == 'Quản lý':
            # Do hệ số lương đang ở dạng str chính vì vậy cần chuyển qua float để tính toán
            he_so_luong = float(str(person['Hệ số lương']).replace(',', ''))
            employee = Manager(person['Mã số'], person['Họ tên'], he_so_luong, person['Số ngày làm việc'],
                               person['Mã bộ phận'], person['Hệ số hiệu quả'], person['Thưởng'],
                               person['Số ngày đi muộn'])

            for department in lst_departments:
                if department['Mã bộ phận'] == person['Mã bộ phận']:
                    bonus_salary = float(str(department['Thưởng bộ phận']).replace(',', ''))

        # Sau khi có đầy đủ thông số để thêm vào class rồi tiến hành tính lương
        bonus_department = Department(person['Mã bộ phận'], bonus_salary)
        salary = employee.calculate_salary(bonus_department)
        # Xong tất các các công thức tiến hành in tất các lương của nhân viên
        print("Mã số: ", person['Mã số'])
        print(f"Thu nhập thực nhận: {salary:,} (VNĐ)")
        print("_" * 30)


def chinh_sua_thong_tin_nhan_vien():
    files_data_persons = "data_persons.json"
    try:
        with open(files_data_persons, 'r', encoding='utf-8') as json_file_data_persons:
            lst_persons = json.load(json_file_data_persons)
    except FileNotFoundError:
        lst_persons = []

    # Tạo hàm để kiểm tra giá trị mới nhập vào là dương hay âm, và nếu không nhập gì thì sẽ nhận lại giá trị cũ
    def input_float_with_default(prompt, old_value):
        while True:
            try:
                value = input(prompt)
                if value.strip() == "":
                    return old_value
                else:
                    return float(value)
            except ValueError:
                print("Bạn cần nhập đúng định dạng số hoặc để trống.")

    # Lập danh sách những ID nhân viên hiện tại đang có trong file được lưu
    lst_id = [person['Mã số'] for person in lst_persons]

    print("Chỉnh sửa nhân viên")
    chon = input("Nhập mã nhân viên: ")
    if chon not in lst_id:
        print("Nhân viên không tồn tại")
    else:
        save_chon = lst_id.index(chon)

        # Sau khi có được số thứ tự nhân viên thông tin muốn chỉnh sửa rồi thì ta sẽ tiến hành lấy dữ liệu và chỉnh sửa thông tin

        print(f"Nhập thông tin mới cho nhân viên có mã số {chon}:")
        new_name = input("Nhập họ và tên (bỏ trống nếu không cần thay đổi): ")
        if new_name:
            lst_persons[save_chon]['Họ tên'] = new_name

        new_position = input("Nhập chức vụ (NV/QL) (bỏ trống nếu không cần thay đổi): ")
        if new_position:
            lst_persons[save_chon]['Chức vụ'] = new_position

        new_salary_coefficient = input_float_with_default(
            "Nhập hệ số lương (bỏ trống nếu không cần thay đổi): ", lst_persons[save_chon]['Hệ số lương'])
        lst_persons[save_chon]['Hệ số lương'] = new_salary_coefficient

        new_work_days = input_float_with_default(
            "Nhập số ngày làm việc (bỏ trống nếu không cần thay đổi): ", lst_persons[save_chon]['Số ngày làm việc'])
        lst_persons[save_chon]['Số ngày làm việc'] = new_work_days

        new_effectiveness_coefficient = input_float_with_default(
            "Nhập hệ số hiệu quả (bỏ trống nếu không cần thay đổi): ", lst_persons[save_chon]['Hệ số hiệu quả'])
        lst_persons[save_chon]['Hệ số hiệu quả'] = new_effectiveness_coefficient

        new_bonus = input_float_with_default(
            "Nhập thưởng (bỏ trống nếu không cần thay đổi): ", lst_persons[save_chon]['Thưởng'])
        lst_persons[save_chon]['Thưởng'] = new_bonus

        new_late_days = input_float_with_default(
            "Nhập số ngày đi muộn (bỏ trống nếu không cần thay đổi): ", lst_persons[save_chon]['Số ngày đi muộn'])
        lst_persons[save_chon]['Số ngày đi muộn'] = new_late_days

        print("_" * 50)
        # Sau khi nhập thông tin mới thành công in ra thông tin mới
        print("Thông tin mới của nhân viên:")
        for key, value in lst_persons[save_chon].items():
            print(f"{key}: {value}")

    # Lưu thông tin sau chỉnh sửa lại vào file JSON
    with open(files_data_persons, 'w', encoding='utf-8') as json_file_data_persons:
        json.dump(lst_persons, json_file_data_persons, ensure_ascii=False, indent=4)


while True:
    print("Menu chức năng:")
    print("1. Hiển thị danh sách nhân viên.")
    print("2. Hiển thị danh sách bộ phận.")
    print("3. Thêm nhân viên mới.")
    print("4. Xóa nhân viên theo ID.")
    print("5. Xóa bộ phận theo ID.")
    print("6. Hiển thị bảng lương.")
    print("7. Chỉnh sửa thông tin của nhân viên")
    print("8. Thoát.")

    chon = input("Mời bạn nhập chức năng mong muốn (từ 1 đến 8): ")
    print('*' * 50)

    if chon == '1':
        hien_thi_danh_sach_nhan_vien()
    elif chon == '2':
        hien_thi_danh_sach_bo_phan()
    elif chon == '3':
        them_nhan_vien_moi()
    elif chon == '4':
        xoa_nhan_vien_theo_id()
    elif chon == '5':
        xoa_bo_phan_theo_id()
    elif chon == '6':
        hien_thi_bang_luong()
    elif chon == '7':
        chinh_sua_thong_tin_nhan_vien()
    elif chon == '8':
        print("Cảm ơn bạn đã sử dụng chương trình.")
        break
    else:
        print("Chức năng không hợp lệ. Vui lòng chọn từ 1 đến 7.")

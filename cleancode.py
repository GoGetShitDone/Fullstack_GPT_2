### --- --- --- --- ###
### --- --- --- --- ###
### --- --- --- --- ###


# 본인이 가장 잘하는 언어로(JS, Python 등등) 더러운 코드를 깨끗한 코드로 리팩토링하는 예시를 만들어보세요. 현재 파일은 JS 로 되어있지만. 자유롭게 다른 언어로 변경해주세요.
# 원칙 1. 함수는 하나의 행동만 해 한다!
"""
# [java 버전]
function emailClients(clients) {
  clients.forEach(client => {
    const clientRecord = database.lookup(client);
    if (clientRecord.isActive()) {
      email(client);
    }
  });
}

"""
# [python 버전]
# Before 😣

import datetime


def send_email_to_client(clients):
    for client in clients:
        client_record = database.lookup(client)
        if client_record.is_active():
            email(client)

# After 😎


def get_active_client(clients):
    active_clients = []
    for client in clients:
        client_record = datavase.lookup(client)
        if client_record.is_active():
            active_clients.append(client)
    return active_clients


def send_emails(clients):
    for client in clients:
        email(client)


def send_email_to_active_client(clients):
    active_cleien = get_active_client(clients)
    send_emails(active_clients)


# 함수는 하나의 행동만 해 한다! = 단일 책임 원칙(Single Responsibility Principle)라는 측면에서 위 함수는 두가지 주요 책임을 지니고 있음
# 1. 기록 조회 / 상태확인 : 데이터베이스에서 기록을 조회 / 클라이언트의 기록이 활성화 상태인지 확인함
# 2. 이메일 발송 : 활성 상태인 클라이언트에게 이메일을 보냄


### --- --- --- --- ###
### --- --- --- --- ###
### --- --- --- --- ###

# 본인이 가장 잘하는 언어로(JS, Python 등등) 더러운 코드를 깨끗한 코드로 리팩토링하는 예시를 만들어보세요. 현재 파일은 JS 로 되어있지만. 자유롭게 다른 언어로 변경해주세요.
# 원칙 2. 함수 명을 통해 함수가 무엇을 하는지 알 수 있어야 한다.

"""
# [java 버전]
# 나쁜 예

function AddToDate(date, month) {
  // ...
}

const date = new Date();

AddToDate(date, 1);

# 좋은 예
function AddMonthToDate(date, month) {
  // ...
}

const date = new Date();
AddMonthToDate(date, 1);

"""
# [python 버전]
# Before 😣


def add_to_date(date, month):
    # ...
    pass


date = datetime.datetime.now()
add_to_date(date, 1)

# ---
# ---
# After 😎


def add_month_to_date(date, month):
    # ...
    pass


date = datetime.datetime.now()
add_month_to_date(date, 1)

# add_to_date 라는 함수 변수에 month 가 있음에도 명칭이 매우 모호함!
# add_month_to_date 라는 이름으로 의미를 더욱 분명하게 처리함!

### --- --- --- --- ###
### --- --- --- --- ###
### --- --- --- --- ###

# 본인이 가장 잘하는 언어로(JS, Python 등등) 더러운 코드를 깨끗한 코드로 리팩토링하는 예시를 만들어보세요. 현재 파일은 JS 로 되어있지만. 자유롭게 다른 언어로 변경해주세요.
# 원칙 3. 중복된 코드 작성하지 마라! 라는 원칙을 통해 공통함수를 추출하고 차이점만 매개변수로 처리!
"""
function showDeveloperList(developers) {
  developers.forEach(developers => {
    const expectedSalary = developer.calculateExpectedSalary();
    const experience = developer.getExperience();
    const githubLink = developer.getGithubLink();
    const data = {
      expectedSalary,
      experience,
      githubLink
    };

    render(data);
  });
}

function showManagerList(managers) {
  managers.forEach(manager => {
    const expectedSalary = manager.calculateExpectedSalary();
    const experience = manager.getExperience();
    const portfolio = manager.getMBAProjects();
    const data = {
      expectedSalary,
      experience,
      portfolio
    };

    render(data);
  });
}

"""
# [python 버전]
# Before 😣


def show_developer_list(developers):
    for developer in developers:
        expected_salary = developer.calculate_expected_salary()
        experience = developer.get_experience()
        github_link = developer.get_github_link()
        data = {
            "expectedSalary": expected_salary,
            "experience": experience,
            "githubLink": github_link
        }

        render(data)


def show_manager_list(managers):
    for manager in managers:
        expected_salary = manager.calculate_expected_salary()
        experience = manager.get_experience()
        portfolio = manager.get_mba_projects()
        data = {
            "expectedSalary": expected_salary,
            "experience": experience,
            "portfolio": portfolio
        }

        render(data)

# ---
# ---
# After 😎


def show_emloyee_data(employees, get_specific_data):
    for employee in employees:
        expected_salary = employee.calculate_expected_salary()
        experience = employee.get_experience()
        specific_data = get_specific_data(employee)
        data = {
            "expectedSalary": expected_salary,
            "experience": experience,
            "specific_data": specific_data
        }
        render(data)


def get_developer_specific_data(developer):
    return developer.get_github_link()


def get_manager_specific_data(manager):
    return manager.ger_mba_projects()


def show_devloper_list(developers):
    show_emloyee_data(employees, get_developer_specific_data)


def show_manager_list(managers):
    show_emloyee_data(employees, get_manager_specific_data)

# 파이썬 코드 강의에서 human 과 player 를 클래스로 나눈 것 처럼 나누려 했으나, 공통 로직을 처리하는 show_emloyee_data 함수로 처리
# 단, 특화된 data 를 처리하는 부분만 별도로 빼어 각각의 직무를 수행하는 직원의 specific_data 를 추출하는 함수를 만들고 출력을 할 때, show_emloyee_data 함수와 결합으로 온전한 data 를 출력

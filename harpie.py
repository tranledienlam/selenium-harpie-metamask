import random
from pathlib import Path
from browser_automation import BrowserManager

from selenium import webdriver
from selenium.webdriver.common.by import By

from browser_automation import Node
from utils import Utility


class Harpie:
    def __init__(self, driver: webdriver.Chrome, profile) -> None:
        self.node = Node(driver, profile['profile'])
        self.driver = driver
        self.profile_name = profile['profile']
        self.password = profile['password']
        self.receive_addresses = profile['receive_addresses']
        self.wallet_url = ''

    def click_button_popup(self, selector: str, text: str = ''):
        Utility.wait_time(5)
        self.node.log(f'Thực hiện execute_script {selector}...')
        try:
            js = f'''
            Array.from(document.querySelectorAll('{selector}')).find(el => el.textContent.trim() === "{text}").click();
            '''
            self.driver.execute_script(js)
        except Exception as e:
            self.node.log(f'click_button_popup {e}')

    def unlock_wallet(self):
        self.node.switch_tab('New Tab', 'title')
        self.driver.get(f'{self.wallet_url}/home.html')
        self.node.log(
            f'Đã chuyển sang tab: {self.driver.title} ({self.driver.current_url})'),

        unlock_actions = [
            (self.node.find_and_input, By.CSS_SELECTOR,
             'input[id="password"]', self.password, 0.1),
            (self.node.find_and_click, By.CSS_SELECTOR,
             'button[data-testid="unlock-submit"]'),
        ]

        if not self.node.execute_chain(actions=unlock_actions, message_error='unlock_wallet'):
            return False

        return True

    def connect_wallet(self):
        '''Chưa dùng, fix khi cần'''
        actions = [
            (self.node.find_and_input, By.CSS_SELECTOR,
             'input[id="email-input"]', self.email, 0.1),
            (self.node.find_and_click, By.XPATH,
             '//p[text()="Don\'t send me marketing emails"]'),
            (self.node.find_and_click, By.XPATH,
             '//button[span[text()="Continue"]]'),
            (self.node.find_and_click, By.XPATH,
             '//button[span[text()="Connect Wallet"]]'),
        ]

        if not self.node.execute_chain(actions=actions):
            self.node.stop(f'connect_wallet')

        els_shadowroot = [
            (By.CSS_SELECTOR, "w3m-modal.open"),
            (By.CSS_SELECTOR, "w3m-router"),
            (By.CSS_SELECTOR, "w3m-connect-view"),
            (By.CSS_SELECTOR, "w3m-wallet-login-list"),
            (By.CSS_SELECTOR, "w3m-connect-announced-widget"),
            (By.CSS_SELECTOR, '[name="OKX Wallet"]')
        ]

        okx_wallet = self.node.find_in_shadow(els_shadowroot)
        if not okx_wallet:
            self.node.stop(f'connect_wallet Không tồn tại Okx wallet để click')

        okx_wallet.click()

        self.node.switch_tab(value='OKX Wallet', type='title')
        self.node.find_and_click(By.XPATH, '//div[text()="Connect"]')
        self.node.switch_tab(value='https://harpie.io/', type='url')

        if self.driver.title.lower().startswith('Application error: a client-side exception has occurred'.lower()):
            self.driver.refresh()

    def scan_wallet(self):
        self.node.find_and_click(By.CSS_SELECTOR,
                                 'button[id="tab-overview-navigator"]')

        if not self.node.find_and_click(By.XPATH,
                                        '//button[text()="Scan Wallet"]', None, 60):
            self.node.log(f'Kiểm tra đã thực hiện scan wallet chưa?')

        if self.node.find(By.XPATH,
                          '//p[text()="You have great wallet security and are safe from most common threats."]',
                          None, 30):
            self.node.log(f'Đã thực hiện Scan wallet')
            return True

        self.node.log(f'Scan wallet thất bại. (Có thể do load trang chậm)')
        return False

    def connect_authentication(self):
        '''Chưa dùng, fix khi cần'''
        self.node.find_and_click(
            By.CSS_SELECTOR, 'button[id="tab-2FA-navigator"]')
        self.node.find_and_click(By.XPATH, '//button[text()="Connect"]')
        self.node.switch_tab('Okx wallet', 'title')
        self.node.find_and_click(By.XPATH, '//div[text()="Approve"]')

        self.node.switch_tab('https://harpie.io/app/dashboard', 'url')

    def send_token(self):
        # chuyển tab chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html
        self.node.switch_tab(f'{self.wallet_url}/home.html', 'url')
        # check tx trước đã hoàn thành chưa? nếu chưa thì ngừng
        if self.node.find(By.CLASS_NAME, 'transaction-status-label'):
            times = 10
            found = False
            while times > 0:
                status_tx = self.node.get_text(
                    By.CLASS_NAME, 'transaction-status-label')
                if status_tx in ['Confirmed', 'Failed']:
                    found = True
                    break
                # Pending thì check Aprove bên harpie và confirm
                if status_tx == 'Pending':
                    self.node.switch_tab(
                        'https://harpie.io/app/dashboard/', 'url')
                    if not self.node.find_and_click(By.XPATH, '//button[span[text()="Approve"]]'):
                        return False

                    self.node.switch_tab(
                        f'{self.wallet_url}/notification.html', 'url')

                    current_handle = self.driver.current_window_handle

                    self.click_button_popup('button[aria-label="Scroll down"]')
                    self.click_button_popup('button', 'Confirm')

                    Utility.wait_time(5)

                    if not current_handle in self.driver.window_handles:
                        self.node.log('Tx token thành công')
                        return True

            times = times - 1
            Utility.wait_time(2)
            if not found:
                self.node.log(f'Tx trước chưa hoàn thành')
                return False
        # chọn mạng Harpi Poly chưa? //div[text()="Harpie Polygon RPC"]

        self.node.find_and_click(By.XPATH, '//button[text()="Tokens"]')
        self.node.find_and_click(By.XPATH, '//span[text()="MATIC"]')
        self.node.find_and_click(
            By.CSS_SELECTOR, 'button[data-testid="coin-overview-send"]')
        self.node.find_and_input(
            By.CSS_SELECTOR, 'input[data-testid="ens-input"]', random.choice(self.receive_addresses), 0)
        self.node.find_and_input(
            By.CSS_SELECTOR, 'input[data-testid="currency-input"]', '0.0001')
        self.node.find_and_click(By.XPATH, '//button[text()="Continue"]')
        self.node.find_and_click(By.XPATH, '//button[text()="Confirm"]')

        self.node.switch_tab('https://harpie.io/app/dashboard/', 'url')
        self.node.find_and_click(By.XPATH, '//button[span[text()="Approve"]]')

        self.node.switch_tab(f'{self.wallet_url}/notification.html', 'url')

        current_handle = self.driver.current_window_handle

        self.click_button_popup('button[aria-label="Scroll down"]')
        self.click_button_popup('button', 'Confirm')

        Utility.wait_time(5)

        if not current_handle in self.driver.window_handles:
            self.node.log('Tx token thành công')
            return True

        self.node.log('Lỗi - Tx token thất bại')
        return False

    def _run_logic(self):
        self.node.switch_tab('MetaMask Offscreen Page', 'title')
        self.wallet_url = "/".join(self.node.get_url().split('/')[:3])

        # unlock wallet
        if not self.unlock_wallet():
            self.node.stop(f'unlock_wallet Thất bại')

        # truy cập dashboard. auto chuyển https://harpie.io/app/dashboard
        self.node.new_tab('https://harpie.io/onboarding/basic/')

        # chuyển sang mạng Poly trên web

        # scan wallet hằng ngày
        self.scan_wallet()

        # vào menu Wallet 2F Authentication để connect
        self.node.find_and_click(
            By.CSS_SELECTOR, 'button[id="tab-2FA-navigator"]')
        # button connect poly trên web?

        # floop send token
        times = 4
        for i in range(0, times):
            self.node.log(f'Bắt đầu lần send_token [{i+1}/{times}]')
            if not self.send_token():
                self.node.log(f'Hoàn thành {i}/{times}')
                self.node.stop(f'send_token thất bại')

            if (i + 1) == times:
                self.node.log(f'Hoàn thành {i+1}/{times}')


class Main:
    def __init__(self, driver, profile) -> None:
        self.profile = profile
        self.driver = driver

    def _run(self):
        Harpie(self.driver, self.profile)._run_logic()


if __name__ == '__main__':
    DATA_DIR = Path(__file__).parent/'data.txt'

    if not DATA_DIR.exists():
        print(f"File {DATA_DIR} không tồn tại. Dừng mã.")
        exit()

    PROFILES = []
    num_parts = 3

    with open(DATA_DIR, 'r') as file:
        data = file.readlines()

    for line in data:
        parts = [p for p in line.strip().split('|') if p]
        if len(parts) < num_parts:
            print(f"Warning: Dữ liệu không hợp lệ - {line}")
            continue

        profile, password, * \
            _ = (parts + [None] * num_parts)[:num_parts]

        PROFILES.append({
            'profile': profile,
            'password': password,
            'receive_addresses': _
        })

    manager = BrowserManager(Main)
    manager.config_extension('meta-wallet-*.crx')
    # manager.run_browser(PROFILES[1])
    manager.run_terminal(
        profiles=PROFILES,
        auto=False,
        max_concurrent_profiles=4
    )

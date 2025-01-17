# -*- coding: utf-8 -*-

from .qt_core import *
from .flat_widgets import *
from .kirikiri_part import KirikiriPart
from .artemis_part import ArtemisPart
from .majiro_part import MajiroPart


class GamePage(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.icon_folder = Path(sys.argv[0]).parent/'Icons'
        self.initUI()
        self.switch_kirikiri()

    def initUI(self):
        self.setup_layouts()
        self.setup_connections()

    def setup_layouts(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        # layout.setSpacing(0)

        self.setup_top_bar()
        layout.addWidget(self.top_bar)

        self.setup_input_folder()
        layout.addWidget(self.input_folder_frame)

        self.setup_output_folder()
        layout.addWidget(self.output_folder_frame)

        self.setup_game_engine_area()
        layout.addWidget(self.game_engine_area)

        self.setup_info_area()
        layout.addWidget(self.info_area_frame)

        self.setup_run_part()
        layout.addWidget(self.run_part_frame)

    def setup_connections(self):
        self.kirikiri_btn.clicked.connect(self.switch_kirikiri)
        self.artemis_btn.clicked.connect(self.switch_artemis)
        self.majiro_btn.clicked.connect(self.switch_majiro)
        self.select_input_folder_btn.clicked.connect(self.choose_input_folder)
        self.select_output_folder_btn.clicked.connect(self.choose_output_folder)
        self.select_input_folder_line_edit.textChanged.connect(self.auto_fill_output_folder)

    def setup_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setMaximumHeight(35)
        self.top_bar.setMinimumHeight(35)
        top_bar_layout = QHBoxLayout(self.top_bar)
        top_bar_layout.setContentsMargins(10, 0, 10, 0)
        top_bar_layout.setSpacing(20)
        self.kirikiri_btn = FPushButton(text='KiriKiri 2/Z', height=self.top_bar.height(), btn_pressed='yellow', text_padding=0, text_align='center', border_direction='border', border_radius=15, border_width=3)
        self.artemis_btn = FPushButton(text='Artemis', height=self.top_bar.height(), btn_pressed='yellow', text_padding=0, text_align='center', border_direction='border', border_radius=15, border_width=3)
        self.majiro_btn = FPushButton(text='Majiro', height=self.top_bar.height(), btn_pressed='yellow', text_padding=0, text_align='center', border_direction='border', border_radius=15, border_width=3)
        top_bar_layout.addWidget(self.kirikiri_btn)
        top_bar_layout.addWidget(self.artemis_btn)
        top_bar_layout.addWidget(self.majiro_btn)

    def setup_input_folder(self):
        self.input_folder_frame = QFrame()
        hlayout = QHBoxLayout(self.input_folder_frame)
        hlayout.setContentsMargins(10, 20, 10, 0)
        self.select_input_folder_lb = QLabel('输入路径')
        self.select_input_folder_lb.setStyleSheet("font: 700 12pt 'Segoe UI'")
        hlayout.addWidget(self.select_input_folder_lb)
        self.select_input_folder_line_edit = FLineEdit(place_holder_text='选择或拖拽需要处理的文件夹', height=30, radius=12, text_padding=10)
        hlayout.addWidget(self.select_input_folder_line_edit)
        self.select_input_folder_btn = FPushButton(height=30, icon_path=self.icon_folder/'icon_folder_open.svg')
        hlayout.addWidget(self.select_input_folder_btn)

    def choose_input_folder(self):
        path_text = QFileDialog.getExistingDirectory()
        if path_text:
            # 转换为操作系统支持的路径格式
            format_path_text = Path(path_text).to_str
            self.select_input_folder_line_edit.setText(format_path_text)

    def setup_output_folder(self):
        self.output_folder_frame = QFrame()
        hlayout = QHBoxLayout(self.output_folder_frame)
        hlayout.setContentsMargins(10, 10, 10, 20)
        self.select_output_folder_lb = QLabel('输出目录')
        self.select_output_folder_lb.setStyleSheet("font: 700 12pt 'Segoe UI'")
        hlayout.addWidget(self.select_output_folder_lb)
        self.select_output_folder_line_edit = FLineEdit(height=30, radius=12)
        self.select_output_folder_line_edit = FLineEdit(place_holder_text='指定输出文件夹', height=30, radius=12, text_padding=10)
        hlayout.addWidget(self.select_output_folder_line_edit)
        self.select_output_folder_btn = FPushButton(height=30, icon_path=self.icon_folder/'icon_folder.svg')
        hlayout.addWidget(self.select_output_folder_btn)

    def auto_fill_output_folder(self):
        output_folder_path = Path(self.select_input_folder_line_edit.text().strip()).parent/'VNU_OUTPUT'
        # while output_folder_path.exists():
        #     output_folder_path = output_folder_path.with_name(output_folder_path.name+'_Output')
        self.select_output_folder_line_edit.setText(str(output_folder_path))

    def choose_output_folder(self):
        path_text = QFileDialog.getExistingDirectory()
        if path_text:
            # 转换为操作系统支持的路径格式
            format_path_text = Path(path_text).to_str
            self.select_output_folder_line_edit.setText(format_path_text)

    def setup_game_engine_area(self):
        self.game_engine_area = QStackedWidget()
        # self.game_engine_area.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.kirikiri = KirikiriPart()
        self.kirikiri.setObjectName('Kirikiri')
        self.game_engine_area.addWidget(self.kirikiri)

        self.game_engine_area.setMaximumHeight(245)

        self.artemis = ArtemisPart()
        self.artemis.setObjectName('Artemis')
        self.game_engine_area.addWidget(self.artemis)

        self.majiro = MajiroPart()
        self.majiro.setObjectName('Majiro')
        self.game_engine_area.addWidget(self.majiro)

    def reset_engine_selection(self):
        for btn in self.top_bar.findChildren(QPushButton):
            try:
                btn.set_active(False)
            except:
                pass

    def setup_info_area(self):
        self.info_area_frame = QFrame()
        # self.info_area_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self.info_area_frame)
        layout.setContentsMargins(10, 0, 10, 0)
        self.info_text_edit = QTextEdit()
        # self.info_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.info_text_edit.setReadOnly(True)
        self.info_text_edit.setStyleSheet('background-color:#333')
        layout.addWidget(self.info_text_edit)

    def setup_run_part(self):
        self.run_part_frame = QFrame()
        layout = QHBoxLayout(self.run_part_frame)
        layout.setContentsMargins(10, 0, 10, 20)

        self.status_progress_bar = FProgressBar(height=30, border_radius=12.5)
        layout.addWidget(self.status_progress_bar)

        self.run_btn = FIconButton(text="开始处理", minimum_width=150, height=30, icon_path=self.icon_folder/'icon_send.svg')
        layout.addWidget(self.run_btn)

    def set_running_state(self, state):
        if state == 0:
            self.run_btn.setEnabled(True)
            self.run_btn.setText('开始处理')
            self.run_btn.set_icon(self.icon_folder/'icon_send.svg')
            self.status_progress_bar.setRange(0, 100)
            self.status_progress_bar.setValue(0)
        elif state == 1:
            self.run_btn.setDisabled(True)
            self.run_btn.setText('正在处理')
            self.run_btn.set_icon(self.icon_folder/'clock.svg')
            self.status_progress_bar.setRange(0, 0)
        elif state == 2:
            self.run_btn.setDisabled(True)
            self.run_btn.setText('正在处理')
            self.run_btn.set_icon(self.icon_folder/'clock.svg')
            self.status_progress_bar.setRange(0, 100)
        elif state == 3:
            self.run_btn.setEnabled(True)
            self.run_btn.setText('开始处理')
            self.run_btn.set_icon(self.icon_folder/'icon_send.svg')
            self.status_progress_bar.setRange(0, 100)
            self.status_progress_bar.setValue(100)

    def switch_kirikiri(self):
        if not self.kirikiri_btn.is_active:
            self.reset_engine_selection()
            self.kirikiri_btn.set_active(True)
            self.game_engine_area.setCurrentWidget(self.kirikiri)

    def switch_artemis(self):
        if not self.artemis_btn.is_active:
            self.reset_engine_selection()
            self.artemis_btn.set_active(True)
            self.game_engine_area.setCurrentWidget(self.artemis)

    def switch_majiro(self):
        if not self.majiro_btn.is_active:
            self.reset_engine_selection()
            self.majiro_btn.set_active(True)
            self.game_engine_area.setCurrentWidget(self.majiro)

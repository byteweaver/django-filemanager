from django.dispatch import Signal


filemanager_pre_upload = Signal(providing_args=["filepath"])
filemanager_post_upload = Signal(providing_args=["filepath"])

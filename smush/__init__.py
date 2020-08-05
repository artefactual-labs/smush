import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from smush.git_log_style_checker import GitLogStyleChecker
from smush.topicmerge import CurrentRepo, TopicMerge

__version__ = "0.0.6"

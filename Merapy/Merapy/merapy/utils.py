import os
from os.path import dirname, realpath

from urllib.parse import urlparse, urljoin

from flask import request, url_for, redirect

from scrapyd_api import ScrapydAPI

from merapy.models import ProjectSpider

from jinja2 import FileSystemLoader, Environment


def transform(s):
    new_s = ''
    for j in s:
        if j == '\'' or j == '\"':
            new_s += '\\\''
        else:
            new_s += j
    return new_s


def which_server():
    pass


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='base.index', **kwargs):  # 重定向登录之前的页面
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def write_setting(project_id):
    spider_config_map = {
        'cfg.tmp': '../scrapy.cfg',
        'settings.tmp': 'settings.py',
        'rules.tmp': 'rules.py',
        'items.tmp': 'custom_settings.py',
    }
    template_dir = dirname(realpath(__file__)) + '/spider_tmp/'
    path = dirname(realpath(__file__)) + '/../../ScrapyUniversal/ScrapyUniversal/'

    env = Environment(loader=FileSystemLoader(template_dir))

    project = ProjectSpider.query.filter_by(id=project_id).first()

    for tmp, output_py in spider_config_map.items():
        with open(path + output_py, 'w', encoding='UTF-8') as f:
            f.write(env.get_template(tmp).render(project=project))
            f.close()
    # 上传
    os.chdir(path + '../')
    os.system('scrapyd-deploy')


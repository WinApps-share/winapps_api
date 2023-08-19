from flask import Blueprint, request, jsonify
import requests
from urllib.parse import urlparse
from urllib.parse import unquote
import os
from dotenv import load_dotenv

info_bp = Blueprint('info', __name__)

@info_bp.route('/info',methods=['POST'])
def software_info():
    name = request.args.get('name')
    # time = request.form.get('time')
    # 构建 URL
    url = f"https://raw.githubusercontent.com/WinApps-share/WinApps-bucket/master/bucket/{name}.json"
    # 发送请求获取数据
    response = requests.get(url)
    data = response.json()

    # 获取 version 和 homepage 字段
    version = data.get('version')
    homepage = data.get('homepage')

    filename_64bit = None
    filename_32bit = None
    hash_64bit = None
    hash_32bit = None
    url_64bit = None
    url_32bit = None

    # 判断根节点是否存在 "url" 和 "hash"
    if 'url' in data and 'hash' in data:
        url_32bit = data.get('url')
        url_32bit.split('#')[0]
        hash_32bit = data.get('hash')
        url_64bit = None
        hash_64bit = None

        parsed_url_32bit = urlparse(url_32bit)
        filename_32bit = unquote(parsed_url_32bit.path.split('/')[-1])
        # filename_64bit = None

    else:
        # 获取 "architecture" 字段下的数据
        architecture = data.get('architecture', {})
        
        # 获取 "64bit" 和 "32bit" 下的数据
        architecture_64bit = architecture.get('64bit', {})
        architecture_32bit = architecture.get('32bit', {})

        if architecture_64bit:
            url_64bit = architecture_64bit.get('url')
            url_64bit = url_64bit.split('#')[0]
            hash_64bit = architecture_64bit.get('hash')
            parsed_url_64bit = urlparse(url_64bit)
            filename_64bit = unquote(parsed_url_64bit.path.split('/')[-1])
        if architecture_32bit:
            url_32bit = architecture_32bit.get('url')
            url_32bit = url_32bit.split('#')[0]
            hash_32bit = architecture_32bit.get('hash')
            parsed_url_32bit = urlparse(url_32bit)
            filename_32bit = unquote(parsed_url_32bit.path.split('/')[-1])
    
    load_dotenv()
    # Get GitHub Token from environment variable
    github_token = os.environ.get("GITHUB_TOKEN")

    if github_token is None:
        raise ValueError("GitHub Token is not set in the environment variable 'GITHUB_TOKEN'")
    # GitHub API endpoint
    repo_owner = "WinApps-share"
    repo_name = "WinApps-bucket"
    path = f"bucket/{name}.json"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={path}"
    
    headers = {
        "User-Agent": "winapps_api",  # Replace with an appropriate User-Agent
        "Authorization": f"token {github_token}"
    }

    response = requests.get(api_url, headers=headers)
    commits = response.json()

    if commits:
        latest_commit = commits[0]
        commit_date = latest_commit.get("commit", {}).get("committer", {}).get("date")
    else:
        commit_date = None

    # 将需要的字段返回为 JSON 格式
    response_data = {
        "version": version,
        "homepage": homepage,
        "date": commit_date,
        "64bit": {
            "hash": hash_64bit,
            "url": url_64bit,
            "filename": filename_64bit
        },
        "32bit": {
            "hash": hash_32bit,
            "url": url_32bit,
            "filename": filename_32bit
        }
    }

    return jsonify(response_data), 200
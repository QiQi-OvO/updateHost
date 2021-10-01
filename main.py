import platform, time, os
import webbrowser
from urllib import request
from urllib.error import HTTPError
from lxml import etree
import ssl


def get_url():
    github_url_lists = [
        "github.com",
        "github.global.ssl.fastly.net",
        "assets-cdn.github.com",
        "raw.githubusercontent.com",
        "codeload.github.com",
        "github.githubassets.com",
        "central.github.com",
        "camo.githubusercontent.com",
        "github.map.fastly.net",
        "gist.github.com",
        "github.io",
        "api.github.com",
        "user-images.githubusercontent.com",
        "favicons.githubusercontent.com",
        "avatars5.githubusercontent.com",
        "avatars4.githubusercontent.com",
        "avatars3.githubusercontent.com",
        "avatars2.githubusercontent.com",
        "avatars1.githubusercontent.com",
        "avatars0.githubusercontent.com",
        "avatars.githubusercontent.com",
        "github-cloud.s3.amazonaws.com",
        "github-com.s3.amazonaws.com",
        "github-production-release-asset-2e65be.s3.amazonaws.com",
        "github-production-user-asset-6210df.s3.amazonaws.com",
        "github-production-repository-file-5c1aeb.s3.amazonaws.com",
        "githubstatus.com",
        "github.community",
        "media.githubusercontent.com",


    ]
    request_urls = []
    for url in github_url_lists:
        request_urls.append("https://" + url + ".ipaddress.com")
    return request_urls,github_url_lists


def get_ip(github_url_lists, url_length):
    ips = []
    count = 1
    try:
        context_ignore = ssl._create_unverified_context()
        for url in github_url_lists:
            time.sleep(0.1)
            if count < url_length:
                end_str = 'Searching ip'
            else:
                end_str = 'Search complete\n'
            process_bar(count / url_length, start_str='', end_str=end_str, total_length=15)
            r = request.urlopen(url, context=context_ignore)
            page = r.read().decode()
            # <td><ul class="comma-separated"><li>140.82.114.3</li></ul></td>
            ips.append(etree.HTML(page).xpath('.//td/ul[@class="comma-separated"]/li/text()')[0])
            count += 1
    except HTTPError as er:
        print(er.code)
    return ips


def update_host_file(hosts, urls, ips):
    hosts_file = open(hosts, 'r')
    line = hosts_file.readline()
    start_index = -1
    end_index = -1
    count = -1
    while line:
        count += 1
        if line.strip() == "# Github Hosts":
            start_index = count
        if line.strip() == "# End of the Github Hosts section":
            end_index = count
        line = hosts_file.readline()
    hosts_file.close()
    if start_index != -1 and end_index != -1:
        hosts_file = open(hosts, 'r+')
        lines = hosts_file.readlines()
        # 更改lines
        del lines[start_index + 1:end_index]
        print("本次更新日期：" + time.strftime("%Y-%m-%d", time.localtime()))
        lines.insert(start_index + 1, "#update:" + time.strftime("%Y-%m-%d", time.localtime()) + "\n")
        insert_index = start_index + 2
        ips = ips[::-1]
        urls = urls[::-1]
        for ip, url in zip(ips, urls):
            lines.insert(insert_index, ip + " " + url + "\n")
        hosts_file.seek(0)
        hosts_file.writelines(lines)
        hosts_file.close()
        print("更新成功")
        return 1
    else:
        print("请在hosts文件中添加一行# Github Hosts 和一行# End of the Github Hosts section 表明Github映射块"
              + "\n例如hosts文件中应该有如下两行:\n # Github Hosts \n # End of the Github Hosts section ")
        return 0


def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m" % '--'] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


if __name__ == '__main__':
    sys_name = platform.system()
    github_urls = []
    request_urls = []
    ips = []
    if sys_name == 'Windows':
        hosts = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
    else:
        hosts = '/etc/hosts'
    print("current os is:" + sys_name + "\nwhere is host:" + hosts)
    request_urls,github_urls = get_url()
    ips = get_ip(request_urls,len(request_urls))
    flag = update_host_file(hosts, github_urls, ips)
    if sys_name == 'Windows' and flag == 1:
        result = os.system('ipconfig /flushdns')
        webbrowser.open("www.github.com", new=0, autoraise=True)
    else:
        # linux刷新 dns指令
        pass
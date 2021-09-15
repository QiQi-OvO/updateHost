import platform, socket , time


def get_url():
    github_url_lists = [
        "github.com",
        "assets-cdn.github.com",
        "assets-cdn.github.com",
        "assets-cdn.github.com",
        "assets-cdn.github.com",
        "github.global.ssl.fastly.net",
        "gist.github.com",
        "cloud.githubusercontent.com",
        "camo.githubusercontent.com",
        "training.github.com",
        "assets-cdn.github.com",
        "documentcloud.github.com",
        "help.github.com",
        "githubstatus.com",
        "github.global.ssl.fastly.net",
        "raw.github.com",
        "raw.githubusercontent.com",
        "cloud.githubusercontent.com",
        "gist.githubusercontent.com",
        "marketplace-screenshots.githubusercontent.com",
        "repository-images.githubusercontent.com",
        "user-images.githubusercontent.com",
        "desktop.githubusercontent.com",
        "avatars.githubusercontent.com",
        "avatars0.githubusercontent.com",
        "avatars1.githubusercontent.com",
        "avatars2.githubusercontent.com",
        "avatars3.githubusercontent.com",
        "avatars4.githubusercontent.com",
        "avatars5.githubusercontent.com",
        "avatars6.githubusercontent.com",
    ]
    return github_url_lists


def get_ip(github_url_lists):
    github_ip_lists = []
    for i in  github_url_lists:
        github_ip_lists.append(socket.gethostbyname(i))
    return github_ip_lists


def update_host_file(hosts,urls,ips):
    hosts_file = open(hosts,'r')
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
        line= hosts_file.readline()
    hosts_file.close()
    if start_index != -1 and end_index != -1:
        hosts_file = open(hosts, 'r+')
        lines = hosts_file.readlines()
        #更改lines
        del lines[start_index+1:end_index]
        print("本次更新日期："+time.strftime("%Y-%m-%d",time.localtime()))
        lines.insert(start_index+1,"#update:"+time.strftime("%Y-%m-%d",time.localtime())+"\n")
        insert_index = start_index + 2
        ips = ips[::-1]
        urls = urls[::-1]
        for ip,url in zip(ips,urls):
            lines.insert(insert_index,ip+" "+url+"\n")
        hosts_file.seek(0)
        hosts_file.writelines(lines)
        hosts_file.close()
        print("更新成功")
    else:
        print("请在hosts文件中添加一行# Github Hosts 和一行# End of the Github Hosts section 表明Github映射块"
              +"\n例如hosts文件中应该有如下两行:\n # Github Hosts \n # End of the Github Hosts section ")
        return


if __name__ == '__main__':
    sys_name = platform.system()
    github_urls = []
    ips = []
    if sys_name == 'Windows':
        hosts = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
    else:
        hosts = '/etc/hosts'

    print("current os is:" + sys_name + "\nwhere is host:" + hosts)
    github_urls = get_url()
    ips = get_ip(github_urls)
    print(ips)
    update_host_file(hosts,github_urls,ips)
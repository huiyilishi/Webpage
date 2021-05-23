from urllib.parse import urlencode,parse_qs,urlparse

#show_data,show_page = page(data=[], all_count=80, cur_page=request.GET.get("page"),request=request.path,params=request.build_absolute_uri())
def page(data=[], half_count=5, all_count=0,
         page_count=20, cur_page=-1,base_url="",params={},
         page_code="page",cur_page_status="current",
         request=None
         ):

    if request:
        base_url = request.path if not base_url else base_url
        params = request.build_absolute_uri() if not params else params
        cur_page = request.GET.get(page_code,"page") if cur_page == -1 else cur_page

    def cur_href(base_url,params,cur_count_page):
        if cur_count_page == cur_page:
            return "javascript:;"
        if type(params) == str:
            query = urlparse(params).query
            params = {k:v[0] for k,v in parse_qs(query).items()}

        if page_code:
            params[page_code] = cur_count_page
        url_params = urlencode(params)
        if "?" in base_url:
            base_url += "&" + url_params
        else:
            base_url += "?" + url_params
        return base_url

    def get_current(cur_page,page):
        if cur_page == page:
            return cur_page_status
        return ""

    def get_num(page):
        # return f"""&nbsp;{page}&nbsp;"""
        return f"""{page}"""

    span_href = ""

    if all_count == 0:
        all_count = len(data)

    try:
        cur_page = int(cur_page)
    except Exception as e:
        cur_page = 1

    if cur_page == 1:
        # span_href += """<span class="unprev"></span>"""
        span_href += """<li class="page-item disabled"><a href="javascript:;" class="page-link" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>"""
    else:
        span_href += f"""<li class="page-item"><a href="{cur_href(base_url,params,cur_page-1)}" class="page-link prev"><span aria-hidden="true">«</span></a></li>"""

    l, r = divmod(all_count, page_count)
    if r != 0:
        l += 1

    if cur_page > l:
        cur_page = l
    elif cur_page < 1:
        cur_page = 1

    if l > half_count * 2:
        if cur_page <= half_count:
            for count in range(1, half_count + 1 + cur_page):
                span_href += f"""<li class="page-item {get_current(cur_page,count)}"><a href="{cur_href(base_url,params,count)}" class="page-link {get_current(cur_page,count)}">{get_num(count)}</a></li>"""

            if cur_page+half_count+1 != l:
                span_href += """<li class="page-item"><a href="javascript:;" class="page-link ">...</a></li>"""
                span_href += f"""<li class="page-item"><a class="page-link " href="{cur_href(base_url,params,l)}" >{get_num(l)}</a></li>"""
        elif cur_page >= l - half_count:
            if l - half_count - 1 != 1:
                span_href += f"""<li class="page-item"><a class="page-link " href="{cur_href(base_url,params,1)}" >{get_num(1)}</a></li>"""
                span_href += """<li class="page-item"><a href="javascript:;" class="page-link ">...</a></li>"""

            for count in range(cur_page - half_count, l + 1):
                span_href += f"""<li class="page-item {get_current(cur_page,count)}"><a href="{cur_href(base_url,params,count)}" class="page-link {get_current(cur_page,count)}">{get_num(count)}</a></li>"""
        else:
            if cur_page - half_count != 1:
                span_href += f"""<li class="page-item"><a class="page-link " href="{cur_href(base_url,params,1)}" >{get_num(1)}</a></li>"""
                span_href += """<li class="page-item"><a href="javascript:;" class="page-link ">...</a></li>"""
            for count in range(cur_page - half_count,cur_page+half_count+1):
                span_href += f"""<li class="page-item {get_current(cur_page,count)}"><a href="{cur_href(base_url,params,count)}" class="page-link {get_current(cur_page,count)}">{get_num(count)}</a></li>"""
            if cur_page+half_count+1 != l:
                span_href += """<li class="page-item"><a href="javascript:;" class="page-link ">...</a></li>"""
                span_href += f"""<li class="page-item"><a class="page-link " href="{cur_href(base_url,params,l)}" >{get_num(l)}</a></li>"""
    else:
        for count in range(1,l+1):
            span_href += f"""<li class="page-item {get_current(cur_page,count)}"><a href="{cur_href(base_url,params,count)}" class="page-link {get_current(cur_page,count)}">{get_num(count)}</a></li>"""

    if cur_page == l:
        # span_href += """<span class="unnext"></span>"""
        span_href += """<li class="page-item disabled"><a href="javascript:;" class="page-link" aria-label="Next"><span aria-hidden="true">»</span></a></li>"""
    else:
        span_href += f"""<li class="page-item"><a href="{cur_href(base_url,params,cur_page+1)} page-link" class="page-link"><span aria-hidden="true">»</span></a></li>"""

    # print(span_href)

    # span_href = f"""<div id="page" class="page" style="display:block;"><div class="page_num">{span_href}</div></div>"""
    span_href = f"""<nav class="pagination-outer" aria-label="Page navigation"><ul class="pagination">{span_href}</ul></nav>"""

    if all_count == 0:
        return 0,0,span_href
    return (cur_page - 1) * page_count,cur_page * page_count,span_href

def get_css():
    css = """<style type="text/css">.pagination-outer{ text-align: center; }
    .pagination{
        display: inline-flex;
        border-radius: 0;
        overflow: hidden;
        position: relative;
    }
    .pagination li a.page-link{
        width: 45px;
        height: 45px;
        line-height: 35px;
        background: #ff095c;
        border-radius: 0;
        border: none;
        outline: 2px solid #fff;
        outline-offset: -6px;
        //font-size: 20px;
        font-weight: 700;
        color: #fff;
        letter-spacing: 1px;
        margin: 0 8px 0 0;
        position: relative;
        z-index: 1;
        transition: all 0.4s ease 0s;
    }
    .pagination li:first-child a.page-link,
    .pagination li:last-child a.page-link{ line-height: 32px; }
    .pagination li:last-child a.page-link{ margin-right: 0; }
    .pagination li.active a.page-link,
    .pagination li a.page-link:hover,
    .pagination li.active a.page-link:hover{
        background: #ff095c;
        color: #fff;
        outline: thin dotted;
        outline-offset: -2px;
    }
    .pagination li a.page-link:before{
        content: "";
        width: 0;
        height: 0;
        background: rgba(0, 0, 0, 0) linear-gradient(135deg, #081f3c 45%, #aaa 50%, #ccc 56%, #fff 80%);
        box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.4);
        position: absolute;
        top: 0;
        left: 0;
        transition: all 0.3s ease 0s;
    }
    .pagination li a.page-link:hover:before,
    .pagination li.active a.page-link:before{
        width: 17px;
        height: 17px;
    }
    @media only screen and (max-width: 480px){
        .pagination{ display: block; }
        .pagination li{
            display: inline-block;
            margin-bottom: 10px;
        }
    }
</style>"""
    return css

if __name__ == "__main__":
    page(data=[], all_count=580,cur_page=12)
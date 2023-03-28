from django.http import JsonResponse

# Create your views here.
class Edp(object):
    def __init__(self):
        pass

    def teach_assess(self, request):
        """教学评估表"""
        if request.method == "GET":
            data = [
                {
                    "title": "教学态度",
                    "content": [
                        "老师教学投入、有激情",
                        "老师教学认真、耐心、诚恳、友好"
                    ]
                }, {
                    "title": "教学内容",
                    "content": [
                        "课程主题明确，内容清晰，论证严密",
                        "课程内容实践性强，案例新"
                    ]
                }, {
                    "title": "教学效果",
                    "content": [
                        "达到预期要求，学习有效，对工作或成长提供帮助",
                        "学习了掌握新思维或新技能"
                    ]
                }, {
                    "title": "教务组织",
                    "content": [
                        "教学课程资料准备充分",
                        "教务组织的规范性、服务质量"
                    ]
                }
            ]
            return JsonResponse({
                "code": 200,
                "data": data
            })

        elif request.method == "POST":
            # 主讲教师
            teacher_txt = request.POST.get("teacher")
            # 课程名称
            course_txt = request.POST.get("course")
            # 上课班级
            class_txt = request.POST.get("class")
            # 上课时间
            time_txt = request.POST.get("time")
            # 教学态度
            attitude_lst = request.POST.get("attitude")
            # 教学内容
            content_lst = request.POST.get("content")
            # 教学效果
            effect_lst = request.POST.get("effect")
            # 教务组织
            organization_lst = request.POST.get("organization")
            # 课程评价
            appraise_txt = request.POST.get("appraise")
            # 课程建议
            recommend_txt = request.POST.get("recommend")
            # 签名
            signature_txt = request.POST.get("signature")

            print("主讲教师: ", teacher_txt)
            print("课程名称: ", course_txt)
            print("上课班级: ", class_txt)
            print("上课时间: ", time_txt)
            print("教学态度: ", attitude_lst)
            print("教学内容: ", content_lst)
            print("教学效果: ", effect_lst)
            print("教务组织: ", organization_lst)
            print("课程评价: ", appraise_txt)
            print("签名: ", signature_txt)

            return JsonResponse({
                "code": 200,
                "data": "OK"
            })

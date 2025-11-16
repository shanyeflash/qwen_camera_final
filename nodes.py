import torch
import nodes

class QWENCameraControl:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 移动控制组 - 改为滑块形式
                "移动控制": ("BOOLEAN", {"default": True}),
                "将镜头向前移动": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "将镜头向左移动": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "将镜头向右移动": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "将镜头向下移动": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                
                # 角度控制组
                "角度控制": ("BOOLEAN", {"default": True}),
                "向左移动角度": ("INT", {"default": 0, "min": 0, "max": 180, "step": 5, "display": "slider"}),
                "向右移动角度": ("INT", {"default": 0, "min": 0, "max": 180, "step": 5, "display": "slider"}),
                "向左旋转角度": ("INT", {"default": 0, "min": 0, "max": 180, "step": 5, "display": "slider"}),
                "向右旋转角度": ("INT", {"default": 0, "min": 0, "max": 180, "step": 5, "display": "slider"}),
                "向下俯视角度": ("INT", {"default": 0, "min": 0, "max": 180, "step": 5, "display": "slider"}),
                "向前旋转角度": ("INT", {"default": 0, "min": 0, "max": 180, "step": 5, "display": "slider"}),
                "向后旋转角度": ("INT", {"default": 0, "min": 0, "max": 180, "step": 5, "display": "slider"}),
                
                # 镜头类型组
                "镜头模式": ([
                    "标准模式",
                    "专业镜头",
                    "4视图展示"
                ], {"default": "标准模式"}),
                
                # 专业镜头类型（当镜头模式为"专业镜头"时显示）
                "专业镜头类型": ([
                    "标准镜头", "广角镜头", "俯视镜头", "仰视镜头", 
                    "特写镜头", "微距镜头", "近景镜头", "远景镜头"
                ], {"default": "标准镜头"}),
                
                # 4视图类型（当镜头模式为"4视图展示"时显示）
                "四视图类型": ([
                    "完整四视图",
                    "正面视图",
                    "侧面视图", 
                    "背面视图",
                    "半侧面视图"
                ], {"default": "完整四视图"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("提示词",)
    FUNCTION = "generate_prompt"
    CATEGORY = "QWEN相机"

    def generate_prompt(self, 移动控制, 将镜头向前移动, 将镜头向左移动, 将镜头向右移动, 将镜头向下移动,
                       角度控制, 向左移动角度, 向右移动角度, 向左旋转角度, 向右旋转角度, 向下俯视角度, 
                       向前旋转角度, 向后旋转角度, 镜头模式, 专业镜头类型, 四视图类型):
        
        prompt_parts = []
        
        # 处理移动控制
        if 移动控制:
            if 将镜头向前移动 == 1:
                prompt_parts.append("镜头向前平移移动")
            if 将镜头向左移动 == 1:
                prompt_parts.append("镜头向左平移移动")
            if 将镜头向右移动 == 1:
                prompt_parts.append("镜头向右平移移动")
            if 将镜头向下移动 == 1:
                prompt_parts.append("镜头向下平移移动")
        
        # 处理角度控制
        if 角度控制:
            if 向左移动角度 > 0:
                prompt_parts.append(f"镜头向左移动{向左移动角度}度")
            if 向右移动角度 > 0:
                prompt_parts.append(f"镜头向右移动{向右移动角度}度")
            if 向左旋转角度 > 0:
                prompt_parts.append(f"镜头向左旋转{向左旋转角度}度")
            if 向右旋转角度 > 0:
                prompt_parts.append(f"镜头向右旋转{向右旋转角度}度")
            if 向下俯视角度 > 0:
                prompt_parts.append(f"镜头向下俯视{向下俯视角度}度")
            if 向前旋转角度 > 0:
                prompt_parts.append(f"镜头向前旋转{向前旋转角度}度")
            if 向后旋转角度 > 0:
                prompt_parts.append(f"镜头向后旋转{向后旋转角度}度")
        
        # 处理镜头模式
        if 镜头模式 == "专业镜头":
            if 专业镜头类型 != "标准镜头":
                lens_map = {
                    "广角镜头": "广角镜头视角，视野开阔，景深效果明显",
                    "俯视镜头": "俯视角度拍摄，自上而下视角，展现整体布局",
                    "仰视镜头": "仰视角度拍摄，自下而上视角，突出主体高度",
                    "特写镜头": "特写镜头，聚焦细节，主体占据画面主要部分",
                    "微距镜头": "微距摄影，极致细节展现，纹理清晰可见",
                    "近景镜头": "近景拍摄，主体突出，背景适度虚化",
                    "远景镜头": "远景拍摄，主体与背景协调"
                }
                prompt_parts.append(lens_map[专业镜头类型])
                
        elif 镜头模式 == "4视图展示":
            view_map = {
                "完整四视图": "四视图正交投影展示，包含前视图、侧视图、后视图、顶视图，工程制图标准，比例精确，线条清晰",
                "正面视图": "正面正交视图，主体正面完整展现，对称结构清晰，中心构图",
                "侧面视图": "侧面正交视图，主体侧面轮廓展现，深度维度明确，侧视角度",
                "背面视图": "背面正交视图，主体背面结构展示，后部细节完整",
                "半侧面视图": "45度半侧视图，立体感强，前后关系明确，透视自然"
            }
            prompt_parts.append(view_map[四视图类型])
        
        # 如果没有选择任何操作，使用默认提示词
        if not prompt_parts:
            return ("标准镜头视角",)
        
        # 组合提示词
        final_prompt = "，".join(prompt_parts) + "。"
        
        return (final_prompt,)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "QWENCameraControl": QWENCameraControl
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QWENCameraControl": "🎮 QWEN相机控制"
}
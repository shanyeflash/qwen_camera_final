import torch
import nodes

class QWENCameraControl:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 视角控制组 - 改为滑块形式
                "视角控制": ("BOOLEAN", {"default": True}),
                "仰视视角": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "俯视视角": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "广角视角": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "特写视角": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "远景视角": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                
                # 角度控制组
                "角度控制": ("BOOLEAN", {"default": True}),
                "向左旋转角度": ("INT", {"default": 0, "min": 0, "max": 90, "step": 5, "display": "slider"}),
                "向右旋转角度": ("INT", {"default": 0, "min": 0, "max": 90, "step": 5, "display": "slider"}),
                "向下俯视角度": ("INT", {"default": 0, "min": 0, "max": 90, "step": 5, "display": "slider"}),
                
                # 专业视图控制组
                "专业视图控制": ("BOOLEAN", {"default": False}),
                "完整的四视图": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "正面视图": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "侧面视图": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "背面视图": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                "半侧面视图": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1, "display": "slider"}),
                
                # 绘画风格选择组（直接保留，不再需要总开关）
                "单色线稿风格": ("BOOLEAN", {"default": False}),
                "插画卡通风格": ("BOOLEAN", {"default": False}),
                "三维渲染动漫风格": ("BOOLEAN", {"default": False}),
                "Q版卡通风格": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("提示词",)
    FUNCTION = "generate_prompt"
    CATEGORY = "QWEN相机"

    def generate_prompt(self, 视角控制, 仰视视角, 俯视视角, 广角视角, 特写视角, 远景视角,
                       角度控制, 向左旋转角度, 向右旋转角度, 向下俯视角度,
                       专业视图控制, 完整的四视图, 正面视图, 侧面视图, 背面视图, 半侧面视图,
                       单色线稿风格, 插画卡通风格, 三维渲染动漫风格, Q版卡通风格):
        
        prompt_parts = []
        
        # 处理视角控制
        if 视角控制:
            if 仰视视角 == 1:
                prompt_parts.append("低角度拍摄，仰视视角")
            if 俯视视角 == 1:
                prompt_parts.append("高角度拍摄，俯视视角")
            if 广角视角 == 1:
                prompt_parts.append("广角镜头，广阔视野")
            if 特写视角 == 1:
                prompt_parts.append("特写镜头，细节聚焦")
            if 远景视角 == 1:
                prompt_parts.append("远景拍摄，远距离视角")
        
        # 处理角度控制
        if 角度控制:
            if 向左旋转角度 > 0:
                prompt_parts.append(f"相机向左旋转{向左旋转角度}度")
            if 向右旋转角度 > 0:
                prompt_parts.append(f"相机向右旋转{向右旋转角度}度")
            if 向下俯视角度 > 0:
                prompt_parts.append(f"相机向下倾斜{向下俯视角度}度")
        
        # 处理专业视图控制
        if 专业视图控制:
            if 完整的四视图 == 1:
                prompt_parts.append("正投影四视图，前视图、侧视图、后视图、顶视图")
            if 正面视图 == 1:
                prompt_parts.append("正面正交视图")
            if 侧面视图 == 1:
                prompt_parts.append("侧面正交视图")
            if 背面视图 == 1:
                prompt_parts.append("背面正交视图")
            if 半侧面视图 == 1:
                prompt_parts.append("半侧面视图，四十五度角")
        
        # 处理绘画风格选择（直接判断，不再需要总开关）
        if 单色线稿风格:
            prompt_parts.append("单色线稿风格，简洁轮廓，单色画风格")
        if 插画卡通风格:
            prompt_parts.append("插画风格，卡通渲染，鲜艳色彩")
        if 三维渲染动漫风格:
            prompt_parts.append("三维渲染动漫风格，卡通着色")
        if Q版卡通风格:
            prompt_parts.append("Q版风格，超级变形比例，可爱卡通")
        
        # 如果没有选择任何操作，使用默认提示词
        if not prompt_parts:
            return ("标准相机视角，正常视图",)
        
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
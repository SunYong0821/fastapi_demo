from agno.agent import Agent
from agno.team import Team
from agno.workflow import Workflow
from agno.workflow.step import Step
from agno.models.vllm import VLLM
from agno.models.llama_cpp import LlamaCpp
from textwrap import dedent
from knowledge import db, whu_db, ksd_project_db, ksd_sample_db

def build_whu_workflow(enable_thinking: bool) -> Workflow:
    retriever = Agent(
        id="retriever-whu-agent",
        model=LlamaCpp(id="qw3.6-27b", base_url="http://localhost:8800/v1/", api_key='EMPTY',extra_body={"chat_template_kwargs": {"enable_thinking": enable_thinking}}),
        instructions=dedent("""\
            # 作为一个专业的知识检索专家。你的任务是:

            **重要规则**:
            1. 仔细理解用户查询
            2. 从知识库中检索最相关的信息
            3. 如果找到了信息，将问题放到 query 字段，将资料和来源整理到 results 字段
            4. 如果没找到信息，将 relevant 字段设置为 false
            **必须输出严格的 JSON 格式**
            """),
        db=db,
        knowledge=whu_db,
        search_knowledge=True
    )

    responder = Agent(
        id="responder-whu-agent",
        model=LlamaCpp(id="qw3.6-27b", base_url="http://localhost:8800/v1/", api_key='EMPTY',extra_body={"chat_template_kwargs": {"enable_thinking": enable_thinking}}),
        instructions=dedent("""
            # 作为一个专业的临床医学专家，你的任务是基于检索结果提供准确、专业的回答。

            **重要规则**:
            1. 仅基于提供的检索结果回答问题，不要编造知识库外的信息
            2. 仔细检查 relevant 字段：
               - 如果为 false ，委婉告知用户该问题不在知识库范围内
               - 如果为 true ，仅使用检索结果中的信息回答
            
            ## 输出案例
            ### 当找到相关信息时

            **答案**：[简要回答]
            **解析**：[详细解释，包括原理、机制等]
            **来源**：[列出所有检索信息的来源，重复的来源只输出一个]
            
            ### 当没有找到相关信息时

            **答案**：抱歉，根据现有知识库信息无法回答此问题。
            **解析**：无
            **来源**：无
            """),
        db=db,
        markdown=True
    )

    return Workflow(
        id="whu-workflow-dynamic",
        name="WHU Medical Immune Workflow",
        db=db,
        steps=[
            Step(name="retriever", agent=retriever),
            Step(name="responder", agent=responder)
        ], telemetry=False
    )

def build_ksd_team(enable_thinking: bool) -> Team:
    project_retriever = Agent(
        id="retriever-project",
        name="项目信息专家",
        role="负责查询项目基本信息：检测费用、价格、报告时间、项目的样本要求等",
        model=LlamaCpp(id="qw3.6-27b", base_url="http://localhost:8800/v1/", api_key='EMPTY',extra_body={"chat_template_kwargs": {"enable_thinking": enable_thinking}}),
        instructions=dedent("""\
            # 作为一个专业的知识检索专家。你的任务是:

            **输出规划（严格执行）**:
            0. **识别范围**：仅提取与“单项价格或套餐价格、样本要求、检验方法、临床意义、报告时间和报告模板”相关的内容。
            1. 如果找到了信息并且能回答问题，先总结内容，然后再进行处理：
                - 如果有多个检索结果，必须使用 Markdown 表格输出。
            2. 如果没有找到信息或不能回答问题，委婉告知用户该问题不在知识库范围内。
            3. 仅基于提供的检索结果回答问题，不要编造知识库外的信息。
            """),
        db=db,
        knowledge=ksd_project_db,
        search_knowledge=True, markdown=True
    )

    sample_retriever = Agent(
        id="retriever-sample",
        name="样本前处理专家",
        role="负责查询样本前处理的送样要求和处理方法",
        model=LlamaCpp(id="qw3.6-27b", base_url="http://localhost:8800/v1/", api_key='EMPTY',extra_body={"chat_template_kwargs": {"enable_thinking": enable_thinking}}),
        instructions=dedent("""\
            # 作为一个专业的知识检索专家。你的任务是:

            **输出规划（严格执行）**:
            0. **识别范围**：仅提取“送样管材、样本类型、保存温度、处理步骤和时间要求”等技术细节。
            1. 如果找到了信息并且能回答问题，整理汇总之后回答用户。
            2. 如果没有找到信息或不能回答问题，委婉告知用户该问题不在知识库范围内。
            3. 仅基于提供的检索结果回答问题，不要编造知识库外的信息。
            """),
        db=db,
        knowledge=ksd_sample_db,
        search_knowledge=True, markdown=True
    )

    return Team(
        model=LlamaCpp(id="qw3.6-27b", base_url="http://localhost:8800/v1/", api_key='EMPTY',extra_body={"chat_template_kwargs": {"enable_thinking": enable_thinking}}),
        members=[project_retriever, sample_retriever],
        instructions=dedent("""\
            你是一个信息分发专家。
    
            ## 分发要求：
            仔细理解用户的查询，判断用户的问题类型：
                - 如果是关于检测费用、价格、报告时间、项目的样本要求等，分发给 '项目信息专家'。
                - 如果是关于送样要求、处理方法等，分发给 '样本前处理专家'。
            """),
        respond_directly=True,
        determine_input_for_members=False,debug_mode=True,
        db=db, telemetry=False
    )



from openai import OpenAI
from utils import *


def supervise(task,table):

    my_function=[{"name": "get_thought",
"description": "Complete the intent understanding of the user's task goal by providing good and bad intent table rubrics scores, and the thought of improving the quality of the current intent table.",
"parameters": {"type": "object",
                "properties": {"good_score": {"type": "array", "description": "A list of scores for the good intent table rubrics answer.",
                                            "items":{"type":"integer","description":"The score for each row in the good intent table rubrics answer."}},
                                "bad_score": {"type": "array", "description": "A list of scores for the bad intent table rubrics answer.",
                                            "items":{"type":"integer","description":"The score for each row in the bad intent table rubrics answer."}},
                                "thought": {"type": "string", "description": "Point out suggestions on how to improve the quality of current intent table. Each point is separated by \n."}
                                },
                "required": ["good_score","bad_score","thought"]
                }
}]

    prompt_begin='''# Your task is to evaluate the quality of the intent table by applying the given rubrics to the intent table generated by the AI agent for an intent understanding of the user's initial task goal, and generate thought on how to further improve the intent table quality.

# Rubric instructions
1. There are two types of rubrics, the good intent table rubrics and the bad intent table rubrics.
2. Each type of rubrics contains 10 items, and each item includes a title and description.
3. Each item has a Yes or No statement.
4. Your job is to carefully go through the intent table and the user's initial task goal, and answer Yes to a rubric applicable to the intent table, then give a score of 1-10 to reflect the likelihood of the intent table complying with the rubric. If the rule is not applicable, answer No and give a score of 0.
5. Each rubric is formatted in a table format with 10 rows and two columns: Index|Yes/No.
6. You need to generate thought on how to improve the quality of the current intent table based on good intent table rubrics and against bad intent table rubrics.

# Good intent table rubrics
1. Title: Precise and Relevant Queries
Description: Queries in the intent table should be directly aligned with the user's goal, asking for specific information that enhances the customization and relevance of the response.
2. Title: Comprehensive Option Coverage
Description: The queries should cover a broad range of possibilities related to the user's request without overwhelming them, allowing the user to specify their preferences or requirements in detail for a tailored response.
3. Title: User Engagement and Customization
Description: Effective intent tables encourage user input through structured choices, enhancing the user's engagement and ensuring the results are customized according to their responses.
4. Title: Clarity and Understandability
Description: Queries and options within intent tables must be clearly formulated and understandable to users of different backgrounds or expertise levels, avoiding technical jargon unless appropriate.
5. Title: Logical Question Sequencing
Description: Questions should be ordered in a logical progression, from general to more specific, to guide the user through a natural thought process and gather information in a structured and efficient manner.
6. Title: User-Centric Approach
Description: The design of intent tables should reflect an understanding of the user's perspective, including considerations for their likely knowledge level, preferences, and the context of their request.
7. Title: Goal Alignment
Description: All aspects of the intent table, from queries to options, should align with the user's original task or goal, ensuring that the table's output serves the user's purpose effectively.
8. Title: Anticipation of User Needs
Description: Queries should anticipate potential user needs or questions, addressing them proactively to streamline the process and enhance user satisfaction.
9. Title: Encouragement of Detailed Responses
Description: Queries should be open-ended or provide a wide range of options where applicable, allowing users to offer detailed information that can guide tailored advice more accurately.
10. Title: Alignment with Task Flexibility
Description: Queries and options should demonstrate an understanding of the task's flexibility requirements, tailoring the interaction to accommodate different approaches and solutions.

# Bad intent table rubrics
1. Title: Lack of User-Centered Depth
Description: Intent tables that offer binary (Yes/No) options or overly narrow queries restrict comprehensive understanding of user preferences, missing the opportunity to delve deeply into their specific needs or intentions.
2. Title: Irrelevant Questioning
Description: When questions assume user interests or knowledge they may not have, or introduce unrelated topics, this can misguide the conversation away from the user's original intent and lead to frustration.
3. Title: Missing Tailored Exploration
Description: Failing to inquire about critical factors such as usage context, budget, preferences, and constraints can significantly restrict the relevance of recommendations and information provided to the user.
4. Title: Lack of Clarity and Structure
Description: A lack of clear progression or structured questioning in the intent table can confuse users, leading to inefficient or ineffective interactions that fail to progress towards a helpful conclusion.
5. Title: Over-simplification of Complexity
Description: Simplifying complex tasks or interests into basic explanations or limited exploration opportunities can underestimate the user's background knowledge or inquiry depth, reducing engagement and satisfaction.
6. Title: Missed Essential Queries
Description: An intent table falls short when it omits critical questions that would directly impact the user's goal, such as forgetting to inquire about dietary restrictions in recipe recommendations or budget constraints in planning advice.
7. Title: Misalignment with Initial Intent
Description: Introducing queries or options that pivot away from the user's stated goal can dilute the focus of the intent table, leading to an outcome that may not fulfill the user’s original request.
8. Title: Overlooking User Constraints
Description: Failure to consider user constraints, such as time, budget, or physical limitations, results in recommendations or advice that may be impractical or unattainable, diminishing the table's utility.
9. Title: Premature Specificity
Description: Bad intent tables often dive into overly specific topics or details too early in the interaction, bypassing an opportunity to understand the user's broader goals or context.
10. Title: Assumed Knowledge or Interest
Description: Assuming user knowledge or interest in specific topics without verification can lead to irrelevant queries, making the table less useful and potentially frustrating for users with different backgrounds or interests.


# User's initial task goal: '''


    prompt_end='''# Task:
1. Go through the intent table and the user's initial task goal, and evaluate whether the intent table is helpful in understanding the user's true intent.
2. Answer Y or N only to each rubric.
3. For Yes answers, score from 1-10 (low to high) to reflect how well the intent table applies to the current rubric. For No answer, score 0. 
4. For each rubric, think carefully about your answer.
5. Provide only one confident answer to each rubric.
6. You must output your answers to all 10 items provided in each rubric.
7. By referring to the score of the current intent table on each rubric, as well as the good intent table rubrics and the bad intent table rubrics, generating the thought on how to improve the quality of the current intent table, which can help the AI agent generate an intent table that is more helpful to the user's intent understanding for their task goal.
8. The thought must have details designed to guide the AI agent to dig further into the user's true intentions and be presented in a format of no more than five points. Provide condensed guidance at each point without providing too much detail.

The output format is as follows:
# Output
Good intent rubrics score table:
[A markdown format table of good intent rubrics score, including three attributes: Index, Yes/No, Score]
Bad intent rubrics score table:
[A markdown format table of bad intent rubrics score, including three attributes: Index, Yes/No, Score]
Thought: [Point out suggestions on how to improve the quality of current intent table.]
...

# Answers'''


    prompt=prompt_begin+task+'\n\n# Current intent table:\n'+table+'\n\n'+prompt_end
    format=False
    i=0
    while format==False:
        supervise_response = chat4(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                # {
                #     "role": "user",
                #     "content": ""
                # }

            ],
            temperature=0.7,
            stream=False,
        )
        thought=supervise_response.choices[0].message.content

        struct_thought_response = chat3(
            model="gpt-4-0613",
            messages=[
                {
                    "role": "user",
                    "content": thought
                },
            ],
            functions=my_function,
            # function_call='auto',
            stream=False,
        )
        struct = struct_thought_response.choices[0].message

        if struct.function_call==None:
            print("supervisor again"+str(i))
            i=i+1
            continue
        try:
            struct_thought = json.loads(struct.function_call.arguments)
        except:
            print("supervisor again"+str(i))
            i=i+1
            continue
        if not ('good_score' in struct_thought.keys() and 'bad_score' in struct_thought.keys() and 'thought' in struct_thought.keys()):
            print("supervisor again"+str(i))
            i=i+1
            continue
        format=True
    return thought,struct_thought






def gpt_completion(client, system_prompt, task_prompt, temperature=0.7, model="gpt-4o-mini"):
    '''
    prompt: 
    model: 
    '''
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task_prompt}
        ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
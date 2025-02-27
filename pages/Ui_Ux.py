import streamlit as st
import json 
import requests
import tempfile
import urllib.parse
from utils.create import create_project_func
from utils.getProject import get_project_func
from utils.image_upload import upload_image
from utils.delete import delete_project_func
from utils.update import update_project_func
from utils.contact import get_contact_func,delete_contact_func
url = 'https://api.uriri.com.ng/v1/product-design/get/projects'
base_url="https://api.uriri.com.ng/v1/product-design"

if "query_parameters" not in st.session_state:
    try:
        st.session_state.query_parameters = st._get_query_params()['selected'][0]
    except: 
        st.session_state.query_parameters = ""

if "edit_link" not in st.session_state:
    st.session_state.edit_link=True
    
if "edit_name" not in st.session_state:
    st.session_state.edit_name= True
if "edit_desc" not in st.session_state:
    st.session_state.edit_desc = True
if "editable_project" not in st.session_state:
    st.session_state.editable_project= None
    
if st.session_state.query_parameters == "":
    projects,form_submissions,create_project,delete_project=st.tabs(["Projects ","Form Submissions","create project","delete project"])



    if "project" not in st.session_state:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                data = json.loads(data['projects'])
                st.session_state.project = data
            else:
                st.session_state.project=[]
        except:
            st.session_state.project=[]

    if "messages" not in st.session_state:
        try:
            st.session_state.contact_messages=get_contact_func(base_url=base_url)
        except:
            st.session_state.contact_messages

    if "a" not in st.session_state:
        st.session_state.a=0
        
    if "new_project" not in st.session_state:
        st.session_state.new_project = []


    def pr(base_url,project_id):
        result = delete_project_func(base_url,project_id)
        if result == True:
            st.toast("deleted Project")
        else:
            st.toast("Failed to delete project")



    with projects:
        for project in st.session_state.project:
            p = json.loads(project)
            with st.container(border=True,key=f"{p['_id']}-edit{st.session_state.a}"):
                st.session_state.a= st.session_state.a+1
                st.write(f"name: {p['name']}")
                st.write(f"description: {p['description']}")
                st.link_button("case study Url",url=p['case_study_link'])
                st.link_button("Image",url=p['case_study_image_link'])
                if st.button(f"Edit project {p['name']} {p['_id']} "):
                    st._set_query_params(selected=f"{p['_id']}")
                    st.session_state.a= st.session_state.a+1
                    st.session_state.query_parameters = p['_id']
                    st.rerun()
                    
        
            
        
    with form_submissions:
        for contact_message in st.session_state.contact_messages:
            try:
                with st.container(key=contact_message['_id'],border=True):
                    mail_link = f"mailto:{contact_message['emailAddress']}?subject=Regarding {contact_message['subject']}&body=Dear {contact_message['firstName']},\n\nI hope this message finds you well. I believe you may have sent a contact message through my portfolio. I would appreciate the opportunity to discuss further if you're interested."
                    st.info(f"This form was sent on  {contact_message['currentDate']}")
                    st.write(f"First Name: {contact_message['firstName']}")
                    st.write(f"Last Name: {contact_message['lastName']}")
                    st.write(f"Subject: {contact_message['subject']}")
                    st.write(f"Message: {contact_message['message']}")
                    st.link_button(f"Contact {contact_message['firstName']}",url=mail_link)
                    if st.button(label=f"Delete message from {contact_message['firstName']}- {contact_message['_id']} ",type='primary'):
                        delete_contact_func(base_url=base_url,contact_id=contact_message['_id'])
                        st.toast("Deleted Successfully")
            except:
                st.info("No One has submitted anything yet")
                    



    with create_project:
        with st.form(key="form"):
            st.text_input(label="Name of Project",key="name")
            st.text_input(label="Link to case Study",key="case_study")
            st.text_area(label="Description of Project",key="description")
            st.file_uploader("Upload image",key="file")
            if st.form_submit_button("Create Project"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    temp_file.write(st.session_state.file.getvalue())
                    temp_file_path = temp_file.name 
                    image_link = upload_image(temp_file_path)
                    
                    result =create_project_func(base_url=base_url,name=st.session_state.name,description=st.session_state.description,case_study_image_link=image_link,case_study_link=st.session_state.case_study)
                    if result==True:
                        st.toast("New project created")
                        st.session_state.file=None
                        st.session_state.description=None
                        st.session_state.case_study=None
                        st.session_state.name=None
                    else: st.toast(" failed ")
                    

    with delete_project:
        for project in st.session_state.project:
            p = json.loads(project)
            with st.container(border=True,key=f"{p['_id']}-delete{st.session_state.a}"):
                st.session_state.a = st.session_state.a+1
                st.write(f"name: {p['name']}")
                st.write(f"description: {p['description']}")
                st.link_button("case study Url",url=p['case_study_link'])
                st.link_button("Image",url=p['case_study_image_link'])
                if st.button(f"delete {p['name']} - {p['_id']}",type='primary'):
                    print("sa")
                    pr(base_url,p['_id'])
                    








    @st.fragment(run_every=10)
    def reset_data():
        response = requests.get(url)
        form_data=get_contact_func(base_url=base_url)
        st.session_state.contact_new_messages=form_data
        if st.session_state.contact_new_messages != st.session_state.contact_messages:
            st.session_state.contact_messages=form_data
            st.rerun()
        if response.status_code == 200:
                data = response.json()
                data = json.loads(data['projects'])
                st.session_state.new_project = data
                if st.session_state.new_project != st.session_state.project:
                    st.session_state.project = data
                    st.rerun()
        else:
            pass



    reset_data()








else:
    if st.button("back"):
        st.session_state.query_parameters = ""
        st._set_query_params()
        st.rerun()
    if st.session_state.editable_project ==None: 
        st.session_state.editable_project= get_project_func(base_url=base_url,project_id=st.session_state.query_parameters)
   
    st.title(f"Project {st.session_state.editable_project['name']}")
    st.image(image=st.session_state.editable_project['case_study_image_link'])
    st.file_uploader(label="replace Image",key="ri")
    with st.container(key="case study Link",border=True):
        st.text_input(label="change case study Link",value=st.session_state.editable_project['case_study_link'],key='csl',disabled=st.session_state.edit_link)
        if st.button("edit link"):
            st.session_state.edit_link = False
            st.rerun()
    with st.container(key="Project Name",border=True):
        st.text_input(label="Project Name",value=st.session_state.editable_project['name'],disabled=st.session_state.edit_name,key="pn")
        if st.button("edit Project Name"):
            st.session_state.edit_name = False
            st.rerun()
    with st.container(key="Project Desc",border=True):
        st.text_area(label="Project Description",value=st.session_state.editable_project['description'],key="pd",disabled=st.session_state.edit_desc)
        if st.button("edit Project Description"):
            st.session_state.edit_desc = False
            st.rerun()
    if st.button(label="Save Changes"):
        
        if st.session_state.ri==None:
             res= update_project_func(base_url,project_id=st.session_state.editable_project['_id'],
                                      name = None if st.session_state.edit_name else st.session_state.pn
                                      ,description= None if st.session_state.edit_desc else st.session_state.pd
                                      ,case_study_link= None if st.session_state.edit_link else st.session_state.csl)
             
             if res==True:
                st.toast("Updated Project")
                st.session_state.query_parameters = ""
                st._set_query_params()
                st.session_state.editable_project =None
                st.session_state.edit_name=True
                st.session_state.edit_link=True
                st.session_state.edit_desc=True
                st.rerun()
             else:
                st.toast("Didn't update")      

                
        
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    temp_file.write(st.session_state.ri.getvalue())
                    temp_file_path = temp_file.name 
                    ri_image_link = upload_image(temp_file_path)
                    res = update_project_func(base_url,project_id=st.session_state.editable_project['_id'],image_link=ri_image_link,
                                        name = None if st.session_state.edit_name else st.session_state.pn
                                        ,description= None if st.session_state.edit_desc else st.session_state.pd
                                        ,case_study_link= None if st.session_state.edit_link else st.session_state.csl)
                    if res==True:
                        st.toast("Updated Project")
                        st.session_state.query_parameters = ""
                        st._set_query_params()
                        st.session_state.editable_project =None
        
                        st.rerun()  
                    else:
                        st.toast("Didn't update")    

                
        
   
    


































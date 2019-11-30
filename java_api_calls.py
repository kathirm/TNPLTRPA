@get_application_Metadata

    1. http://10.6.4.60:8080/metadata/Application?name=Application 

@Post_MetaData

    1. http://10.6.4.60:8080/metadata/Application
    
    2. format (Content-Type : application/json

            bodyContent)

@Post_geo_Attendance_workflow

    1. http://10.6.4.60:8080/workflow/geoAttendance/start

    2. format({
        "uId":"4",
        "fileName":"M.Ravichandran.1.jpg",
        "attendanceTime":"21-11-2019 20:30:00",
        "latitude":"7.34",
        "longitude":"10.5463"
        })

@start_geo_attendance_workflow

    1. http://10.6.4.18:8082/rest/process-definition/key/geoAttendance/tenant-id/Terafastnet/submit-form

    2. format({"variables":{"username":{"value":"Admin@Terafastnet"},"password":{"value":"!changeme!"},"uId":{"value":"12"},"fileName":{"value":"M.Ravichandran.1.jpg"},"rpaHost":{"value":"rpaHost"},"rpaPort":{"value":"8080"},"attendanceTime":{"value":"15-11-2019 11:30:00"},"latitude":{"value":"10.3452"},"longitude":{"value":"45.5463"},"kafka":{"value":"10.6.4.36"}}})


@face_gecognation_api

    1. http://10.6.4.60:8080/faceRec/5cd675e314068541d8926880/facerec

    2. postman --> send imageFile (Key = file, Value = ImageFile_path)


@get_login_token

    1. http://10.6.4.60:8080/auth/login?username=Admin@Terafastnet&password=!changeme!

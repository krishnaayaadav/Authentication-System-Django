/**  
  This JavaScript files will contains Validation on for Different forms likes signup,login,password others form validations
 */



function SignupFormValidation(){
    let username = document.getElementById('id_username').value;
    let error    = document.getElementById('username');
    let status   =  false;

    if(username == ''){
       error.innerHTML = 'Username is required!';
       return status;

    }
    if(username.length < 4){
        error.innerHTML = 'Username must contains 4 characters!';
        return status;

    }

    let f_name = document.getElementById('first_name').value;

    if(f_name == '' || f_name == undefined){
        error.innerHTML =  'First name  is required! ';
        return status;
       
    }else{
        alert(' else f_name')

    }

   
   
    return true;

   
}   


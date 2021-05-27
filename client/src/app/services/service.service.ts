import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  constructor(private http:HttpClient) { }
  checkLogin(username,password){
    return this.http.post(`http://127.0.0.1:8000/login `, {
      "username":username,
      "password":password
    })
  }
  gettodayBday(){
    return this.http.get(`http://127.0.0.1:8000/today_BD`)
  }
  getreportiesleaves(gotuser){
    return this.http.get(`http://127.0.0.1:8000/reporties_leave?username=${gotuser}`)
  }
  getTaskbyId(TaskID: String, gotuser: any){
    return this.http.get(`http://127.0.0.1:8000/get_TasksbyId?id=${TaskID}&username=${gotuser}`)
  }
   putTask(gotuser,id1,Task,TaskDescription,WorkLink1,Technology){
     return this.http.put(`http://127.0.0.1:8000/Update_Tasks?username=${gotuser}&id=${id1}&Task=${Task}&TaskDescription=${TaskDescription}&WorkLink=${WorkLink1}&Technology=${Technology}`,{})
   }
  getmonthBday(){
    return this.http.get(`http://127.0.0.1:8000/month_BD`)
  }
  holiday(){
    return this.http.get(`http://127.0.0.1:8000/Holidays`)
  }
  DeleteTask(username2: String, TaskID2: String){
    return this.http.delete(`http://127.0.0.1:8000/Tasks?username=${username2}&id=${TaskID2}`)
  }
  private messageSource = new BehaviorSubject('default message');
  currentMessage = this.messageSource.asObservable();

  changeMessage(message: string) {
    this.messageSource.next(message)
  }
  applyleave(startDate,endDate,appliedBy,reason){
    return this.http.post(`http://127.0.0.1:8000/leave`,{
      "startDate":startDate,
      "endDate":endDate,
      "appliedBy":appliedBy,
      "reason":reason
    })
  }
  gettaskbyuser(gotuser: String){
    return this.http.get(`http://127.0.0.1:8000/get_Tasks_byUser?User=${gotuser}`)
  }
  addTask(task,taskdescription,gotuser,technology,WorkLink){
    return this.http.post(`http://127.0.0.1:8000/add_Tasks `, {
      "Task":task,
      "TaskDescription":taskdescription,
      "username":gotuser,
      "Technology":technology,
      "WorkLink":WorkLink,
    })
  }
  signup(firstName,lastName,username,password,DOB,finalImg){
    console.log(firstName,lastName,username,password,DOB,finalImg);
    return this.http.post(`http://127.0.0.1:8000/add_users`,{
      "firstName":firstName,
      "lastName":lastName,
      "username":username,
      "password":password,
      "DOB":DOB,
      "image":finalImg
    })
  }
  Setreportie(gotuser,reportieID){
    return this.http.put(`http://127.0.0.1:8000/set_reportie?username=${gotuser}&reportieId=${reportieID}`,{})
  }
  getallleaves(username){
    return this.http.get(`http://127.0.0.1:8000/leave?username=${username}`)
  }
  getreporties(gotuser){
    return this.http.get(`http://127.0.0.1:8000/get_reporties?username=${gotuser}`)
  }
  updatepassword(username,password,newpassword){
    return this.http.put(`http://127.0.0.1:8000/login`,{
      "username":username,
      "password":password,
      "newpassword":newpassword
    })
  }
  removereportie(gotuser,reportieId){
    return this.http.put(`http://127.0.0.1:8000/remove_reportie?username=${gotuser}&reportieId=${reportieId}`,{})
  }
  Viewreportiestasks(username5,reportieID){
    return this.http.get(`http://127.0.0.1:8000/getA_reportiesTasks?username=${username5}&reportieId=${reportieID}`)
  }
  getuserdetails(username){
    return this.http.get(`http://127.0.0.1:8000/userDetails?username=${username}`)
  }
  getreportiestasks(gotuser){
    return this.http.get(`http://127.0.0.1:8000/get_reportiesTasks?username=${gotuser}`)
  }
  setStatus(gotuser,requestId,message){
    return this.http.put(`http://127.0.0.1:8000/approve_leave?username=${gotuser}&requestId=${requestId}&message=${message}`,{})
  }
  CheckIn(Empnum,finalImg){
    return this.http.post(`http://127.0.0.1:8000/check_in?employeeNumber=${Empnum}&checkInImage=${finalImg}`,{})
  }
  CheckinbyempId(Empnum){
    return this.http.get(`http://127.0.0.1:8000/check_in_by_employeeNumber?employeeNumber=${Empnum}`)
  }
  Checkout(ID,finalImg){
    return this.http.post(`http://127.0.0.1:8000/check_out?id=${ID}&checkOutImage=${finalImg}`,{})
  }
  Addgroup(groupname,description){
    return this.http.post(`http://127.0.0.1:8000/groups`,{
      "groupName": groupname,
      "description": description
    })
  }
  Getgroups(displayuser){
    return this.http.get(`http://127.0.0.1:8000/groups`)
  }
  Deletegroups(_id){
    return this.http.delete(`http://127.0.0.1:8000/groups?id=${_id}`)
  }
  Updategroups(_id,groupname,description){
    return this.http.put(`http://127.0.0.1:8000/group?id=${_id}`,{
      "groupName": groupname,
      "description": description,
    })
  }
  Getroles(){
    return this.http.get(`http://127.0.0.1:8000/roles`)
  }
  Addroles(groupname, username){
    return this.http.post(`http://127.0.0.1:8000/roles`,{
      "groupName": groupname,
     "username": username
    })
  }
  Deleteroles(_id){
    return this.http.delete(`http://127.0.0.1:8000/roles?id=${_id}`)
  }
  Updateroles(_id,groupname){
    return this.http.put(`http://127.0.0.1:8000/role?id=${_id}`,{
      "groupName": groupname
    })
  }
}

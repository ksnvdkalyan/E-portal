import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../services/service.service';
import { Router } from '@angular/router';
import { ThrowStmt } from '@angular/compiler';

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent implements OnInit {
  gotuser: any;
  TaskID: String;

  constructor(private route: Router,private userdata: ServiceService) {
    this.userdata.currentMessage.subscribe(message => this.gotuser = message)
   }
   displayuser = sessionStorage.getItem("username25")
  ngOnInit(): void {
    this.imgvar = sessionStorage.getItem('image');
    this.viewtasks()
    this.viewallleaves()
    this.viewreporteestasks()
    this.getreportie1()
    this.getreportiesLeaves()
    this.getgroups()
    this.getroles()
  }
  imgvar :any = "";
  signOut(){
    sessionStorage.clear();
    this.route.navigate(['']);
  }
  refresh(){
    this.viewtasks()
    this.viewallleaves()
    this.viewreporteestasks()
    this.getreportie1()
    this.getreportiesLeaves()
    this.getgroups()
    this.getroles()
  }
  print
  username
  taskdescription
  technology
  WorkLink
  task
  alltasksarray
  alltasks
  TaskID2
  response1
  taskdetails
  addtask(){
    this.userdata.addTask(this.task,this.taskdescription,this.displayuser,this.technology,this.WorkLink,).subscribe(response =>{
      this.print = response['message'];
    })
  }

  taskToUpdate;
  send(task : String){
    this.taskToUpdate = task;
    console.log("task to update",this.taskToUpdate);
  }
  viewtasks(){
    this.userdata.gettaskbyuser(this.displayuser).subscribe(response=>{
      this.alltasks=response;
    })
  }
  deletetask(){
      this.userdata.DeleteTask(this.displayuser,this.taskToUpdate?._id).subscribe(response=>{
    this.response1=response["message"];
  })
  }
  id1
  Task
  TaskDescription
  WorkLink1
  Technology
  msg
  response2
  startDate
  endDate
  appliedBy
  reason
  allleaves
  updatetask(){
    this.userdata.putTask(this.displayuser, this.taskToUpdate?._id, this.Task, this.TaskDescription, this.WorkLink1, this.Technology).subscribe(response=>{
     this.msg=response["message"]
    })
   }
   addleave(){
      this.userdata.applyleave(this.startDate,this.endDate,this.displayuser,this.reason).subscribe(response=>{
        this.response2=response["message"]
      })
  }
  viewallleaves(){
    this.userdata.getallleaves(this.displayuser).subscribe(response=>{
      this.allleaves=response;
  })
}
newpassword
confirmpassword
password
response3
allreportiestasks
changepassword(){
  if(this.newpassword ==this.confirmpassword){
    this.userdata.updatepassword(this.displayuser,this.password,this.newpassword).subscribe(response=>{
      this.response3=response["message"]
    })
  }
  if (this.newpassword != this.confirmpassword){
    this.response3 = "Password is not the same";
  }
}
  viewreporteestasks(){
      this.userdata.getreportiestasks(this.displayuser).subscribe(response=>{
        this.allreportiestasks=response;
      })
  }
  allreporties
  getreportie1(){
    this.userdata.getreporties(this.displayuser).subscribe(response=>{
      this.allreporties=response;
  })
  }
  allreportiesleaves
  getreportiesLeaves(){
    this.userdata.getreportiesleaves(this.displayuser).subscribe(response=>{
      this.allreportiesleaves=response;
      console.log(this.allreportiesleaves)
    })
  }
  requestId
  message
  response4
  reportieId
  response5
  setstatus(){
    this.userdata.setStatus(this.displayuser,this.taskToUpdate?.id,this.message).subscribe(response=>{
      this.response4=response["message"];
    })
  }
  Removereportie(){
    console.log(this.taskToUpdate?._id)
    this.userdata.removereportie(this.displayuser,this.taskToUpdate?._id).subscribe(response=>{
      this.response5=response["message"];
    })
  }
  reportieID
  response6
  setreportie(){
    this.userdata.Setreportie(this.displayuser,this.reportieID).subscribe(response=>{
      this.response6=response["message"];
    })
  }
  groupname
  description
  response7
  addgroup(){
    this.userdata.Addgroup(this.groupname,this.description).subscribe(response=>{
      this.response7= response["message"];
    })
  }
  response10
  addroles(){
    this.userdata.Addroles(this.groupname, this.username).subscribe(response=>{
      this.response10= response["message"];
    })
  }
  allgroups
  getgroups(){
    this.userdata.Getgroups(this.displayuser).subscribe(response=>{
      this.allgroups = response;
      console.log(this.allgroups)
    })
  }
  allroles
  getroles(){
    this.userdata.Getroles().subscribe(response=>{
      this.allroles = response;
    })
  }
  response8
  removegroup(){
    this.userdata.Deletegroups(this.taskToUpdate?._id).subscribe(response=>{
      this.response8 = response["message"];
    })
  }
  response11
  removerole(){
    this.userdata.Deleteroles(this.taskToUpdate?._id).subscribe(response=>{
      this.response11 = response["message"];
    })
  }
  response9
  updategroup(){
    this.userdata.Updategroups(this.taskToUpdate?._id,this.groupname,this.description).subscribe(response=>{
      this.response9 =response["message"];
    })
  }
  response12
  updaterole(){
    this.userdata. Updateroles(this.taskToUpdate?._id,this.groupname).subscribe(response=>{
      this.response12 =response["message"];
    })
  }
}

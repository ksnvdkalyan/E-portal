import { Component, OnInit } from '@angular/core';
import { RouterLink, Router } from '@angular/router';
import { ServiceService } from '../services/service.service';
import { Subject, Observable } from 'rxjs';
import { WebcamImage, WebcamInitError, WebcamUtil } from 'ngx-webcam';
import {  Output, EventEmitter } from '@angular/core';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  bdayboysdate: any;
  holidaysdate: any;
  holidaysdatearray=[];
  holidaysarray=[];
  holidays: any;
  todaybday: any;
  todaybdayarray=[]
  count: number =0;
  canprint: boolean
  canprint1: boolean

  constructor(private route: Router, private userdata: ServiceService) {
    this.todaybithday()
    this.allbdays()
    this.getholidays()
   }


  todaybithday(){
    this.userdata.gettodayBday().subscribe(response=>{
      this.todaybday = response;
      for(let i=0; i<this.todaybday.length; i++){
        this.todaybdayarray[i]=this.todaybday[i];
        this.count++;
      }
      if(this.count>=1){
        this.canprint = true
      }
      else{
        this.canprint1=true
      }
    })
  }
  allbdays()
  {
    this.userdata.getmonthBday().subscribe(response=>{
      this.bdayboys=response[0];
      this.bdayboysdate=response[1];
      for(let i=0; i<this.bdayboys.length; i++){
        this.bdayboysarray[i]=this.bdayboys[i];
      }
      for(let i=0; i<this.bdayboysdate.length; i++){
        this.bdayboysdatearray[i]=this.bdayboysdate[i];
      }
    });
  }
  getholidays()
  {
    this.userdata.holiday().subscribe(response=>{
      this.holidays=response[0];
      this.holidaysdate=response[1];
      for(let j=0; j<this.holidays.length; j++){
        this.holidaysarray[j]=this.holidays[j];
      }

      for(let j=0; j<this.holidaysdate.length; j++){
        this.holidaysdatearray[j]=this.holidaysdate[j];
      }
    });
  }
  bdayboys
  bdayboysarray=[]
  bdayboysdatearray=[]
  days
  username
  password
  print ="a";
  print2
  cantprint :boolean =false
  checklogin(){
  this.userdata.checkLogin(this.username,this.password).subscribe(response =>{
    this.print = response["token"];
    this.print2 = response;
    console.log(this.print2)
    if(this.print2 == "Authentication Failed"){
      this.cantprint = true;
    }
    if(this.print.length>0)
    {

      sessionStorage.setItem("username25",response['username'])
      sessionStorage.setItem("image",response['image'])
      this.userdata.changeMessage(this.username)
      this.route.navigate(['/content']);
    }
  },error=>{
    this.print = ""
  })
  }
  gotocamera(){
    this.route.navigate(['/checkin']);
  }
  DOB
  firstName
  lastName
  print1

  public webcamImage: WebcamImage = null;
vedio = false;
recap= true;
finalImg: any = "";
@Output()
  public pictureTaken = new EventEmitter<WebcamImage>();
  // toggle webcam on/off
  public showWebcam = true;
  public allowCameraSwitch = true;
  public multipleWebcamsAvailable = false;
  public deviceId: string;
  public videoOptions: MediaTrackConstraints = {
    // width: {ideal: 1024},
    // height: {ideal: 576}
  };
  public errors: WebcamInitError[] = [];
  // webcam snapshot trigger
  private trigger: Subject<void> = new Subject<void>();
  // switch to next / previous / specific webcam; true/false: forward/backwards, string: deviceId
  private nextWebcam: Subject<boolean | string> = new Subject<boolean | string>();
  public ngOnInit(): void {
    WebcamUtil.getAvailableVideoInputs()
      .then((mediaDevices: MediaDeviceInfo[]) => {
        this.multipleWebcamsAvailable = mediaDevices && mediaDevices.length > 1;
      });
  }
  public triggerSnapshot(): void {
    this.trigger.next();
    this.vedio = true;
    this.recap = false;
  }
  public toggleWebcam(): void {
    this.showWebcam = !this.showWebcam;
  }
  public handleInitError(error: WebcamInitError): void {
    this.errors.push(error);
  }
  public showNextWebcam(directionOrDeviceId: boolean | string): void {
    // true => move forward through devices
    // false => move backwards through devices
    // string => move to device with given deviceId
    this.nextWebcam.next(directionOrDeviceId);
  }
  public handleImage(webcamImage: WebcamImage): void {
    console.info('received webcam image', webcamImage);
    // this.pictureTaken.emit(webcamImage);
    this.webcamImage= webcamImage;
    this.finalImg = this.webcamImage.imageAsDataUrl;
  }
  public cameraWasSwitched(deviceId: string): void {
    this.deviceId = deviceId;
  }
  public get triggerObservable(): Observable<void> {
    return this.trigger.asObservable();
  }
  public get nextWebcamObservable(): Observable<boolean | string> {
    return this.nextWebcam.asObservable();
  }

  // handleImage(webcamImage: WebcamImage) {
  // this.webcamImage = webcamImage;
  // }
  recapture(){
    this.showWebcam = true;
    this.vedio = false;
    this.webcamImage = null;
    this.recap = true;
  }
  Signup(){
    this.userdata.signup(this.firstName,this.lastName,this.username,this.password,this.DOB,this.finalImg).subscribe(response =>{
      console.log(this.finalImg)
      this.print1 = response["message"];
      console.log(this.print1)
    })
    }
}

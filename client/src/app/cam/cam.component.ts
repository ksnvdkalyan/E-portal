import { Component, OnInit, Output, EventEmitter } from '@angular/core';
// import {WebcamImage, WebcamInitError, WebcamUtil} from 'ngx-webcam';
import { Subject, Observable } from 'rxjs';
import { WebcamImage, WebcamInitError, WebcamUtil } from 'ngx-webcam';
import { Router } from '@angular/router';
import { ServiceService } from '../services/service.service';

@Component({
  selector: 'app-cam',
  templateUrl: './cam.component.html',
  styleUrls: ['./cam.component.css']
})
export class CamComponent implements OnInit {
  public webcamImage: WebcamImage = null;
vedio = false;
recap= true;
finalImg: any = "";

  constructor(private route: Router, private userdata: ServiceService) { }
  signOut(){
    this.route.navigate(['']);
  }
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
  Empnum: String;
  returnvalue
  checked = "checked-in"
  checkin(){
    this.userdata.CheckIn(this.Empnum,this.finalImg).subscribe(response=>{
      this.returnvalue=response['message']
      this.signOut()
    })
  }
  empdetails
  canshow
  canshow1 : boolean = false;
  getempdetails(){
    this.userdata.CheckinbyempId(this.Empnum).subscribe(response=>{
      this.empdetails=response;
    })
  }
  checkIn: boolean = false
  getcheckin(){
    this.checkIn= true
  }
  changevalues(){
    this.checkIn= false
  }
  taskToUpdate
  send(task : String){
    this.taskToUpdate = task;
    this.checkout= true;
  }
  checkout: boolean = false;
  checkOut(){
    this.userdata.Checkout(this.taskToUpdate?._id,this.finalImg).subscribe(response=>{
      this.returnvalue=response['message'];
      this.signOut()
    })
  }
  storedNum
  send2(){
    this.storedNum=this.Empnum
  }
}

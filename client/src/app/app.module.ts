import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {FormsModule} from "@angular/forms";
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {CamComponent} from './cam/cam.component';
import { ErrorpageComponent } from './errorpage/errorpage.component';
import { HomeComponent } from './home/home.component';
import { ContentComponent } from './content/content.component';
import {HttpClientModule} from '@angular/common/http';
import { WebcamModule } from 'ngx-webcam';

@NgModule({
  declarations: [
    AppComponent,
    ErrorpageComponent,
    CamComponent,
    HomeComponent,
    ContentComponent,
  ],
  imports: [
    FormsModule,
    BrowserModule,
    HttpClientModule,
    WebcamModule,
    AppRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

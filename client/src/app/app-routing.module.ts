import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ErrorpageComponent} from './errorpage/errorpage.component';
import {HomeComponent} from './home/home.component';
import {ContentComponent} from './content/content.component';
import {CamComponent} from './cam/cam.component';
import { GuardGuard } from './guards/guard.guard';


const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'checkin', component: CamComponent},
  {path: 'content', component: ContentComponent, canActivate:[GuardGuard]},
  {path: '**',component: ErrorpageComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

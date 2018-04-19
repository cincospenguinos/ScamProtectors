// src/app/pages/home/home.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';

import { Title } from '@angular/platform-browser';
import { ApiService } from './../../core/api.service';
import { UtilsService } from './../../core/utils.service';
import { Subscription } from 'rxjs/Subscription';
import { VtuModel } from './../../core/models/vtu.model';

import { AuthService } from './../../auth/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit, OnDestroy {
  pageTitle = 'Accounts';
  vtuListSub: Subscription;
  vtuList: VtuModel[];
  loading: boolean;
  error: boolean;

  constructor(
    public utils: UtilsService,
    private api: ApiService,
    private router: Router,
    public auth: AuthService) { }

  ngOnInit() {
    // this._getVtuList();
  }

  // private _getVtuList() {
  public _getVtuList() {
      this.loading = true;
    // Get VTUs
    this.vtuListSub = this.api
      .getVtus$()
      .subscribe(
        res => {
          this.vtuList = res;
          this.loading = false;
        },
        err => {
          console.error(err);
          this.loading = false;
          this.error = true;
        }
      );
  }

  ngOnDestroy() {
    this.vtuListSub.unsubscribe();
  }
}
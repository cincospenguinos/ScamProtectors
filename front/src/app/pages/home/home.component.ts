// src/app/pages/home/home.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';

import { Title } from '@angular/platform-browser';
import { ApiService } from './../../core/api.service';
import { UtilsService } from './../../core/utils.service';
import { Subscription } from 'rxjs/Subscription';
import { VtuModel } from './../../core/models/vtu.model';

import { AuthorizationService } from './../../auth/authorization.service';

import { AuthService, SocialUser, GoogleLoginProvider } from "angular5-social-login";
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit, OnDestroy {
  pageTitle = 'Accounts';
  userSub: Subscription;
  vtuAddSub: Subscription;
  vtuListSub: Subscription;
  vtuFlaggedListSub: Subscription;
  vtuList: VtuModel[];
  vtuFlaggedList: VtuModel[];
  loading: boolean;
  error: boolean;

  private user: SocialUser;
  public authorized: boolean = false;
  result: boolean;

  constructor(
    public utils: UtilsService,
    private api: ApiService,
    private router: Router,
    public auth: AuthorizationService,
    private socialAuth: AuthService,
    private http: HttpClient) { }

  ngOnInit() {
    if (this.auth.loggedIn) {
      this._addCaretaker();
      this._getVtuList();
    }
  }

  signInWithGoogle(): void {
    this.socialAuth.signIn(GoogleLoginProvider.PROVIDER_ID).then(
      (userData) => { //on success
        //this will return user data from google. What you need is a user token which you will send it to the server
        if (userData != null) {
          this.authorized = true;
          this.user = userData;
        }
        this._addVtu(userData.email, userData.idToken);
      }
    );
  }

  private _addCaretaker() {
    this.loading = true;
    this.userSub = this.api
      .postUser$()
      .subscribe(
        res => {
          this.loading = false;
        },
        err => {
          console.error(err);
          this.result = false;
          this.loading = false;
          this.error = true;
        }
      );
  }

  private _getVtuList() {
    this.loading = true;
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

  private _getFlaggedList() {
    this.loading = true;
    this.vtuFlaggedListSub = this.api
      .getFlagged$()
      .subscribe(
        res => {
          this.vtuFlaggedList = res;
          this.loading = false;
        },
        err => {
          console.error(err);
          this.loading = false;
          this.error = true;
        }
      );
  }
  
  private _addVtu(vtuEmail: string, vtuToken: string): void {
    this.vtuAddSub = this.api
      .postVtu$(vtuEmail, vtuToken)
      .subscribe(
        data => {
          this.result = true;
          this.loading = false;
        },
        err => {
          console.error(err);
          this.result = false;
          this.loading = false;
          this.error = true;
        }
      );
  }

  ngOnDestroy() {
    this.vtuListSub.unsubscribe();
    this.vtuAddSub.unsubscribe();
    this.userSub.unsubscribe();
    this.vtuFlaggedListSub.unsubscribe();
  }
}
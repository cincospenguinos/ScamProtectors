// src/app/core/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { AuthorizationService } from './../auth/authorization.service';
import { Observable } from 'rxjs/Observable';
import { catchError } from 'rxjs/operators';
import 'rxjs/add/observable/throw';
import { ENV } from './env.config';
import { VtuModel } from './models/vtu.model';

@Injectable()
export class ApiService {

  constructor(
    private http: HttpClient,
    private auth: AuthorizationService) { }

  private get _authHeader(): string {
    return `Bearer ${localStorage.getItem('access_token')}`;
  }

  // GET list of all authenticated VTUs of current user
  getVtus$(): Observable<VtuModel[]> {
    return this.http
      .get(`${ENV.BASE_API}vtus/` + this.auth.userProfile.email)
      .pipe(
        catchError((error) => this._handleError(error))
      );
  }

  // POST new VTU
  postVtu$(vtuEmail: string, vtuToken: string): Observable<VtuModel> {
    let params = new HttpParams();
    params = params.set('email', vtuEmail);
    params = params.set('token', vtuToken);
    return this.http
      .post(`${ENV.BASE_API}vtus/` + this.auth.userProfile.email, params
      )
      .pipe(
        catchError((error) => this._handleError(error))
      );
  }

  // POST user
  postUser$(): Observable<VtuModel> {
    return this.http
      .post(`${ENV.BASE_API}log-in/` + this.auth.userProfile.email, null)
      .pipe(
        catchError((error) => this._handleError(error))
      );
  }

  // GET list of flagged emails under user
  getFlagged$(): Observable<VtuModel[]> {
    return this.http
      .get(`${ENV.BASE_API}flagged-emails/` + this.auth.userProfile.email)
      .pipe(
        catchError((error) => this._handleError(error))
      );
  }

  private _handleError(err: HttpErrorResponse | any): Observable<any> {
    const errorMsg = err.message || 'Error: Unable to complete request.';
    if (err.message && err.message.indexOf('No JWT present') > -1) {
      this.auth.login();
    }
    return Observable.throw(errorMsg);
  }
}
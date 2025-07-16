; with glavninalog ( Glavninalog1,Količinaglavnognaloga ,Scenario, ShipDate,Prvidatum )

as (

SELECT

t0.U_BXPWODcN  'Glavni nalog',t4.PlannedQty, t0.U_BXPMTOSc 'Scenario', t3.ShipDate , row_number() over (partition by t0.U_BXPMTOSc  order by t3.ShipDate) AS 'Prvi datum'

FROM [dbo].[@BXPMTOORDRSOLREF]  T0 WITH (NOLOCK)

inner join ORDR t2 on t2.Docnum = t0.U_BXPSODcN
inner join RDR1 t3 on t3.DocEntry = t2.DocEntry and t3.LineNum = t0.U_BXPSOLin
inner join owor t4 on t4.DocNum = t0.U_BXPWODcN

WHERE  t0.U_BXPParWR is null and t0.U_BXPOrdTy = 'W'

GROUP BY t0.U_BXPMTOSc, t0.U_BXPWODcN ,t3.ShipDate,t4.PlannedQty


 )

, Sumirano (Item,RN,Naziv,Linija,Operacija,NazivOP,Normamin,Kolicina,Zaprimljenakolicina,Cekirananorma,Masina,NazivMasine,Scenario,Statusrn)

as (
--select t11.Glavninalog1 as 'Glavni nalog KPL', t11.Količinaglavnognaloga 'Količina glavnog naloga',

select t0.ItemCode,t0.DocNum  ,t8.ItemName,t1.LineNum,t1.ItemCode 'OP',t9.ItemName 'OP Naziv',t1.PlannedQty 'Norma min',t0.PlannedQty 'Količina',t0.CmpltQty 'Zaprimljena količina'

,SUM(T12.[U_BXPCoQty]) *  ( t1.PlannedQty / t0.PlannedQty) as 'Čekirana norma min'   ,t10.code 'Mašina',t10.name 'Naziv Masine' ,t0.U_BXPMTOSc,t0.Status


from  OWOR t0 inner join WOR1 t1 on t0.DocEntry = t0.DocEntry
             inner join [@BXPPRODORDERREQU]  T2 on t2.U_BXPPrOOI  = t1.U_BXPBxID and t0.DocEntry = t2.U_BXPPrODE
             inner join  [@BXPPRODORDEROPER] t3 on t3.Code = t1.U_BXPBxId
             left join OITM t8 on t0.ItemCode = t8.ItemCode
             left join OITM t9 on t1.ItemCode = t9.ItemCode
             inner join [dbo].[@BXPWORKCENTER]  t10 on t10.Code =  t2.U_BXPPrfWC
             --left join glavninalog t11 on t11.Scenario = t0.U_BXPMTOSc
             ---and t11.Prvidatum = '1'
             left JOIN [dbo].[@BXPPDCBOOKING]  T12 ON T1.U_BXPBxID = T12.U_BXPPrOOI




where (t0.[Status] = 'r' or t0.[Status] = 'L' )  


and t10.code = 'g1000'


--and (t0.PlannedQty > t0.CmpltQty) 


AND T0.PostDate > '01-01-2019'

group by   t0.Itemcode, t0.DocNum   ,t8.ItemName,t1.ItemCode ,t0.PlannedQty ,t0.CmpltQty , t1.PlannedQty , t0.PlannedQty ,t10.code ,t10.name  ,t0.U_BXPMTOSc,t9.ItemName,t1.LineNum,t0.Status )


select   t11.Glavninalog1 as KPL ,t11.Količinaglavnognaloga AS KPLQ,t0.RN AS RN ,t0.Naziv AS NAZIV,sum(t0.Normamin)AS Norma ,t0.Kolicina as Q,t0.Zaprimljenakolicina ZQ,sum(ISNULL (t0.Cekirananorma ,0))CQ,t0.Masina AS WC,t0.NazivMasine AS WCNAME,t0.Scenario AS MTO ,t11.ShipDate AS Isporuka,t0.Item,t0.Statusrn

from sumirano t0   left join glavninalog t11 on t11.Scenario = t0.Scenario

group by t0.Item,t11.Glavninalog1,t11.Količinaglavnognaloga,RN,Naziv,Kolicina,Zaprimljenakolicina,t0.Scenario ,t11.ShipDate,t0.Masina,t0.NazivMasine,t0.Statusrn

order by t0.Scenario,t0.RN,t0.Naziv

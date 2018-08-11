package com.wyrobnik.coursera_crypto;

import java.math.BigInteger;
import java.util.HashMap;
import java.util.Map;

import javafx.util.Pair;

public class DLog {

  public static final BigInteger B = BigInteger.valueOf(1).shiftLeft(20);
  private static final BigInteger P_DEFAULT = new BigInteger("13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171");
  private static final BigInteger G_DEFAULT = new BigInteger("11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568");
  private static final BigInteger H_DEFAULT = new BigInteger("3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333");

  public final BigInteger p;
  public final BigInteger g;
  public final BigInteger h;

  public static void main(final String[] args) {
    final DLog dlog = new DLog(P_DEFAULT, G_DEFAULT, H_DEFAULT);
    System.out.println(dlog.computeDLog());
  }

  /**
   * @param p the modulo, prime number
   * @param g base
   * @param h argument to dlog
   */
  public DLog(final BigInteger p, final BigInteger g, final BigInteger h) {
    this.p = p;
    this.g = g;
    this.h = h;
  }

  /**
   * Compute the discrete log dlog_g(h) in Z*_p.
   * Meaning find x in `h = g^x (mod p)`.
   * Assumes 1 <= x <= B^2
   *
   * Uses meet in the middle approach:
   * x = x0*B + x1
   * h/(g^x1)  = (g^B)^x0 in Zp
   * For all x1 in B compute h/(g^x1) and memorize
   * For all x0 in B compute (g^B)^x0 until a matching value is found.
   * Using the matching x1 and x0 values, compute x.
   *
   * @return x
   */
  public BigInteger computeDLog() {
    final Map<BigInteger, BigInteger> valuesToX1 = computeAllValuesForX1();
    final Pair<BigInteger, BigInteger> x0x1 = findMatchingX0(valuesToX1);
    final BigInteger x = constructX(x0x1.getKey(), x0x1.getValue());
    return x;
  }

  private Map<BigInteger, BigInteger> computeAllValuesForX1() {
    final Map<BigInteger, BigInteger> output = new HashMap<>();
    BigInteger gpow = BigInteger.ONE;
    BigInteger x1 = BigInteger.ZERO;
    int i = 0;
    while (x1.compareTo(B) <= 0) {
      output.put(
        h.divide(gpow),
        x1
      );
      x1 = x1.add(BigInteger.ONE);
      gpow = gpow.multiply(g).mod(p);
      i+=1;
      if (i == 1000000000) {
        System.out.println("x1: " + x1.toString());
        i = 0;
      }
    }
    return output;
  }

  // Return x0, x1
  private Pair<BigInteger, BigInteger> findMatchingX0(
    final Map<BigInteger, BigInteger> valuesToX1
  ) {
    final BigInteger gb = g.modPow(B, p);
    BigInteger x0 = BigInteger.ZERO;
    BigInteger matchingValue = BigInteger.ONE;
    int i = 0;
    while (x0.compareTo(B) <= 0) {
      if (valuesToX1.containsKey(matchingValue)) {
        break;
      }
      matchingValue = matchingValue.multiply(gb);
      x0 = x0.add(BigInteger.ONE);
      i+=1;
      if (i == 1000000000) {
        System.out.println("x0: " + x0.toString());
        i = 0;
      }
    }
    return new Pair<>(x0, valuesToX1.get(matchingValue));
  }

  private BigInteger constructX(
    final BigInteger x0,
    final BigInteger x1
  ) {
    return x0.multiply(B).add(x1);
  }

}

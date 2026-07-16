import 'package:flutter/material.dart';

import '../models/birth_data.dart';
import '../models/horoscope_result.dart';

class HoroscopeService {
  static Future<HoroscopeResult> generate({
    required String name,
    required DateTime birthDate,
    required TimeOfDay birthTime,
    required String birthPlace,
    required String gender,
  }) async {
    final birth = BirthData(
      name: name,
      gender: gender,
      birthDate: birthDate,
      birthTime: birthTime,
      birthPlace: birthPlace,
    );

    return _calculate(birth);
  }

  static Future<HoroscopeResult> _calculate(
    BirthData birth,
  ) async {
    await Future.delayed(const Duration(milliseconds: 500));

    //
    // TEMPORARY ENGINE
    //
    // This block will be replaced by Swiss Ephemeris.
    //

    final year = birth.birthDate.year;
    final month = birth.birthDate.month;
    final day = birth.birthDate.day;
    final hour = birth.birthTime.hour;

    final ascendants = [
      "Aries",
      "Taurus",
      "Gemini",
      "Cancer",
      "Leo",
      "Virgo",
      "Libra",
      "Scorpio",
      "Sagittarius",
      "Capricorn",
      "Aquarius",
      "Pisces",
    ];

    final signs = [
      "Aries",
      "Taurus",
      "Gemini",
      "Cancer",
      "Leo",
      "Virgo",
      "Libra",
      "Scorpio",
      "Sagittarius",
      "Capricorn",
      "Aquarius",
      "Pisces",
    ];

    return HoroscopeResult(
      ascendant: ascendants[(day + hour) % 12],
      sun: signs[(month + year) % 12],
      moon: signs[(day + month) % 12],
      mercury: signs[(hour + month) % 12],
    );
  }
}
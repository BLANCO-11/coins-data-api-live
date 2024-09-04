package com.rev.demo.Repository;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;
import com.rev.demo.Model.Cryptocurrency;

public interface CryptocurrencyRepository extends JpaRepository<Cryptocurrency, String> {
    Optional<Cryptocurrency> findByName(String name);
}
